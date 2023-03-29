"""
api.py
- provides the API endpoints for consuming and producing
  REST requests and responses
"""

# from flask import Blueprint, request, jsonify
# from models import db

# api = Blueprint('api', __name__)

###################################################
"""
API 1 - 
"""

from flask import Flask, request, jsonify
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

app = Flask(__name__)
CORS(app)

lda_disk=gensim.models.ldamodel.LdaModel.load("model/model_6Topics")
id2word = corpora.Dictionary.load('model/model_Dictionary')

@app.route('/loadmodel', methods=['GET'])
def load_model():
  selected_chap = int(request.args.get('selected_chap'))
  folder = request.args.get('folder')

  # test_corpus = preprocessing.load_corpus('test_data/Chapters/1974')
  test_corpus = preprocessing.load_corpus(folder)
  test_ids = test_corpus.fileids()
  chapters_name = [id.replace('.txt','') for id in test_ids]

  test_docs = preprocessing.corpus2docs(test_corpus)
  test_vecs = preprocessing.docs2vecs(test_docs, id2word)

  # get topic distribution of chapter
  # selected_chap = 0
  vector = lda_disk[test_vecs[selected_chap]]
  sim_topic = max(vector,key=lambda item:item[1])
  top_topic = sim_topic[0]
  topic_word = lda_disk.show_topic(top_topic-1, topn=41050)

  selected_words = [id2word[i[0]] for i in test_vecs[0]]
  selected_words[0:20]

  key_words = []
  for word in topic_word:
      if (len(key_words) < 5) &(word[0] in selected_words):
          key_words.append(word)

  # chosen_chapter = chapters_name[chap_num]
  recommendation_scores = []

  similarity = similarities.MatrixSimilarity(lda_disk[test_vecs])

  for i in range(0,len(test_vecs)):
      vector = lda_disk[test_vecs[i]]
      # sim_topic = max(vector,key=lambda item:item[1])
      
      if(i == selected_chap):
          sims = similarity[vector]
          sims = list(enumerate(sims))
          for sim in sims:
              chapter_num = sim[0]
              recommendation_score = [chapters_name[chapter_num], sim[1]]
              recommendation_scores.append(recommendation_score)
          
  recommendation_scores = sorted(recommendation_scores, key=lambda x: x[1], reverse=True) 
  return jsonify(
     {
        'key_words': [word[0] for word in key_words],
        "recommendation": [chapter[0] for chapter in recommendation_scores[1:4]]
     }
  )
     
  
  # return jsonify({'name': 'John Doe'})

@app.route('/preprocessbook', methods=['GET'])
def preprocessBook():
    books_directory = request.args.get('books_directory')
    filename = request.args.get('filename') + '.txt'
    last_line = request.args.get('lastline')
    dir = books_directory + "/Chapters2"
    chapter_list = []
    book_name = ""

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
          
    # return jsonify({'chapters': 'testing'})
    return jsonify({'book_name': book_name, 'chapters': chapter_list})
    # return jsonify({'book_name': book_name})

  # return jsonify({'recommendation': recommendation_scores[1:4]})
    
@app.route('/splitbook', methods=['GET'])
def splitBook():
  book_name = request.args.get('book_name')
  # text = localStorage.getItem('book_text')
  last_line = request.args.get('lastline')
  chapter_list = []

  # cleaned_text = preprocessing.remove_end(text, last_line)
  # preprocessing.savecleanBooks(cleaned_text, book_name)
  # chap_index = preprocessing.chapIndexes(cleaned_text)
  # split_text = preprocessing.splitbyChapters(cleaned_text, chap_index)
  # if ((type(split_text) == list) & (len(split_text)>1)):
  #     chapter_list = preprocessing.saveChapters(split_text, book_name)
  
  return jsonify({'chapters': 'testing'})
  # return jsonify({'chapters': chapter_list})

if __name__ == '__main__':
  app.run(host='0.0.0.0', port='3000', debug=True)