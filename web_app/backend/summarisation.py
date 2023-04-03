# import libraries
import gensim
from gensim import corpora
from gensim import similarities
from gensim import models
from gensim.models import CoherenceModel

import preprocess
import os
import re

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.cluster.util import cosine_distance

import numpy as np
import networkx as nx

#########################################################################
# get all txt files in the directory
# return:
# book_texts: list of strings, each string is a chapter
# chapters_names: list of strings, each string is the name of the chapter
#########################################################################
def load_chapters(directory):
    book_texts = []
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as f:
                book_texts.append(f.read())
    return book_texts



#########################################################################
# tokenize the chapter into sentences
# return:
# sentences: list of strings, each string is a sentence
#########################################################################
def tokenize_chapter(chapter):
    sentences = nltk.sent_tokenize(chapter)
    return sentences



#########################################################################
# clean the tokenized sentences
# return:
# new_sentence_list: list of cleaned sentences
#########################################################################
def clean_sentences(sentences):
    cleaned_sentence_list = []
    for i in sentences:
        cleaned_sentence = i.replace('\n', ' ')
        cleaned_sentence_list.append(cleaned_sentence.split(' '))
    new_sentence_list = []
    new_sentence_list = [[word for word in sentences if word] for sentences in cleaned_sentence_list]
    return new_sentence_list



#########################################################################
# (1/3) calculate the cosine similarity between two sentences
# return:
# similarity: float, the cosine similarity between two sentences
#########################################################################
def sentence_similarity(sent1, sent2, stopwords=None):
    if stopwords is None:
        stopwords = []
 
    sent1 = [w.lower() for w in sent1]
    sent2 = [w.lower() for w in sent2]
 
    all_words = list(set(sent1 + sent2))
 
    vector1 = [0] * len(all_words)
    vector2 = [0] * len(all_words)
 
    # build the vector for the first sentence
    for w in sent1:
        if w in stopwords:
            continue
        vector1[all_words.index(w)] += 1
 
    # build the vector for the second sentence
    for w in sent2:
        if w in stopwords:
            continue
        vector2[all_words.index(w)] += 1
        
    if np.isnan(1 - cosine_distance(vector1, vector2)):
        return 0
    return 1 - cosine_distance(vector1, vector2)

#########################################################################
# (2/3) build the similarity matrix by using (1/3)
# return:
# similarity_matrix: 2D array, the similarity matrix
#########################################################################
def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix

#########################################################################
# (3/3) generate the summary by using (2/3) and (3/3)
# return:
# summaised_text
#########################################################################
def generate_summary(new_sentences):
    # 1. stop words
    stop_words = stopwords.words('english')
    
    summaised_text = []

    # 2. generate similarity matrix across sentences
    sentence_similarity_matrix = build_similarity_matrix(new_sentences, stop_words)

    # 3. rank sentences in similarity matrix
    sentence_similarity_graph = nx.from_numpy_array(sentence_similarity_matrix)
    scores = nx.pagerank(sentence_similarity_graph)

    # 4. sort the rank and pick top sentences
    ranked_sentence = sorted(((scores[i],s) for i,s in enumerate(new_sentences)), reverse=True)

    # 5. get the summary
    for i in range(3):
        summaised_text.append(" ".join(ranked_sentence[i][1]))
    
    # 6. join the sentences
    summaised_text = " ".join(summaised_text)
    
    return summaised_text