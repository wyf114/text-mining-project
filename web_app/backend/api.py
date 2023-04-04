"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

# from flask import Blueprint, request, jsonify
# from models import db


###################################################
"""
API 1 - 
"""

from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS

import gensim
from gensim import corpora
from gensim import similarities
from gensim import models
from gensim.models import CoherenceModel
from gensim.models.ldamodel import LdaModel
import preprocessing
import pandas as pd
import os
from os import path
import networkx as nx
from nltk.corpus import stopwords

api = Blueprint('api', __name__)

app = Flask(__name__)
CORS(app)

lda_disk=gensim.models.ldamodel.LdaModel.load("model/finalmodel_5Topics")
id2word = corpora.Dictionary.load('model/finalmodel_Dictionary')

@app.route('/loadmodel', methods=['GET'])
def load_model():
  selected_chap = request.args.get('selected_chap')
  folder = request.args.get('folder')
  keyword_type = request.args.get('keyword_type')

  # test_corpus = preprocessing.load_corpus('test_data/Chapters/1974')
  test_corpus = preprocessing.load_corpus(folder)
  test_ids = test_corpus.fileids()
  chapters_name = [id.replace('.txt','') for id in test_ids]
  selected_chap_index = chapters_name.index(selected_chap)

  test_docs = preprocessing.corpus2docs(test_corpus)
  
  bigram = gensim.models.Phrases(test_docs, min_count=5, threshold=50) # higher threshold fewer phrases.
  trigram = gensim.models.Phrases(bigram[test_docs], threshold=50)  
  # Faster way to get a sentence clubbed as a trigram/bigram
  bigram_mod = gensim.models.phrases.Phraser(bigram)
  trigram_mod = gensim.models.phrases.Phraser(trigram)

  docs_bigrams = preprocessing.make_bigrams(bigram_mod, test_docs)
  data_bigrams_trigrams = preprocessing.make_trigrams(bigram_mod, trigram_mod, docs_bigrams)
  test_vecs = preprocessing.docs2vecs(data_bigrams_trigrams, id2word)

  # get topic distribution of chapter
  vector = lda_disk[test_vecs[selected_chap_index]]
  sim_topic = max(vector,key=lambda item:item[1])
  top_topic = sim_topic[0]
  topic_word = lda_disk.show_topic(top_topic, topn=len(id2word))

  selected_words = [id2word[i[0]] for i in test_vecs[selected_chap_index]]
  selected_words[0:20]

  key_words = []
  for word in topic_word:
      if(keyword_type == 'unigrams'):
         if (len(key_words) < 5) & (word [0] in selected_words):
            key_words.append(word)
      else:
        if ('_' in word[0]) & (len(key_words) < 5) & (word [0] in selected_words):
          key_words.append(word)
 
  #  Recommendation
  recommendation_scores = []

  similarity = similarities.MatrixSimilarity(lda_disk[test_vecs])

  for i in range(0,len(test_vecs)):
      vector = lda_disk[test_vecs[i]]
      if(i == selected_chap_index):
          sims = similarity[vector]
          sims = list(enumerate(sims))
          for sim in sims:
              chapter_num = sim[0]
              recommendation_score = [chapters_name[chapter_num], sim[1]]
              recommendation_scores.append(recommendation_score)
          
  recommendation_scores = sorted(recommendation_scores, key=lambda x: x[1], reverse=True) 

  # Summarisation
  
  sentences = preprocessing.splitbySentences(folder, selected_chap)
  stop_words = stopwords.words('english')
  # print(stop_words)
  summarize_text = []
          
  # Step 2 - Generate Similarity Matrix across sentences
  sentence_similarity_matrix = preprocessing.build_similarity_matrix(sentences, stop_words)

  # Step 3 - Rank sentences in similarity matrix
  sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
  scores = nx.pagerank(sentence_similarity_graph)

  # Step 4 - Sort the rank and pick top sentences
  ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)    
 
  # number of sentences to combine
  for i in range(3):
      summarize_text.append(" ".join(ranked_sentence[i][1]))

  
  return jsonify(
     {
        'key_words': [word[0] for word in key_words],
        "recommendation": [chapter[0] for chapter in recommendation_scores[1:4]],
        'summary': ". ".join(summarize_text).replace('..', '.')
     }
  )

@app.route('/preprocessbook', methods=['GET'])
def preprocessBook():
    books_directory = request.args.get('books_directory') #test_data
    filename = request.args.get('filename') + '.txt'
    last_line = request.args.get('lastline')
    dir = books_directory + "/Chapters2" #test_data/Chapters
    chapter_list = []
    
    book_text = ''
    if filename.endswith('.txt'):
      with open(os.path.join(books_directory, filename), "r", encoding="utf8", errors='ignore') as file:
          book_name = filename.replace('.txt','')
          book_text = file.read()

      cleaned_text = preprocessing.remove_end(book_text, last_line)
      preprocessing.savecleanBooks(cleaned_text, book_name)
      chap_index = preprocessing.chapIndexes(cleaned_text)
      split_text = preprocessing.splitbyChapters(cleaned_text, chap_index)
      if ((type(split_text) == list) & (len(split_text)>1)):
          chapter_list = preprocessing.saveChapters(dir, split_text, book_name)

    return jsonify({'book_name': book_name, 'chapters': chapter_list})

########################################################################
# receive the .txt file from frontend
# Things it does:
# 1. split chapters and save to folder
# 2. get chapter name for frontend to put inside the dropdown
# Output:
# 1. chapter_list
########################################################################

@app.route('/upload', methods=['POST'])
def upload():

  # get whatever passed from frontend
  filename = request.files['file'].filename
  last_line = request.form['lastline']
  content = request.files['file'].read()

  # get the filename: e.g.4339
  book_name = filename.replace('.txt','')

  # remove the content of the last line
  content_lastline_removed = preprocessing.remove_end(content.decode("utf-8"), last_line)

  # save the cleaned book to folder
  preprocessing.savecleanBooks(content_lastline_removed, book_name)

  # get the indexes of the chapters
  chap_index = preprocessing.chapIndexes(content_lastline_removed)
  
  # split the book into chapters
  splitted_text = preprocessing.splitbyChapters(content_lastline_removed, chap_index)
  

  # save each chapters to folder
  chapter_list = []
  if ((type(splitted_text) == list) & (len(splitted_text)>1)):
    chapter_list = preprocessing.saveChapters('test_data/Chapters3', splitted_text, book_name)
  
  
  # pass the dir to frontend, cos need this data in next step 'showResult'
  chap_folder = f"test_data/Chapters3/{book_name}"

  # test
  print(chap_folder)

  # return chapter-list to frontend
  return jsonify({
    'chap_folder': chap_folder,
    'chapters': chapter_list
    })


if __name__ == '__main__':
  app.run(host='0.0.0.0', port='3000', debug=True)