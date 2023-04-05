from datetime import datetime
import nltk
from nltk.corpus import stopwords
from nltk.corpus import PlaintextCorpusReader
from nltk.stem.porter import *
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.probability import FreqDist
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

import re

stop_list = stopwords.words('english')        
stop_list += ['project', 'gutenberg', 'ebook', 'www.gutenberg.org', 'from', 'subject', 'would', 'etext', 're', 'edu', 'use', 'http', 'www',
             'said', 'denotes']

def load_corpus(dir):
    # dir is a directory with plain text files to load.
    corpus = nltk.corpus.PlaintextCorpusReader(dir, '.+\.txt')
    return corpus

def corpus2docs(corpus):
    fids = corpus.fileids()
    docs_token = []
    for fid in fids:
        doc_raw = corpus.raw(fid)
        doc = nltk.word_tokenize(doc_raw)
        docs_token.append(doc)

    docs_lower = [[w.lower() for w in doc] for doc in docs_token]
    docs_alpha = [[w for w in doc if re.search('^[a-z]+$', w)] for doc in docs_lower]

    lemmatizer = WordNetLemmatizer()
    docs_lem = [[lemmatizer.lemmatize(word, tag[0].lower()) for word, tag in pos_tag(doc, tagset='universal') if tag[0].lower() in ['a', 'r', 'n', 'v']] for doc in docs_alpha]

    return docs_lem


def docs2vecs(docs, dictionary):
    # docs is a list of documents returned by corpus2docs.
    # dictionary is a gensim.corpora.Dictionary object.
    vecs1 = [dictionary.doc2bow(doc) for doc in docs]
    return vecs1

#####################################################################
from num2words import num2words
import os
from os import path
import shutil

remove_list = ['CONTENTS', 'APPENDIX', 'INDEMNITY', 'PREFACE', 'DEFINITIONS', 'CHAPTER', 'BY', 'ILLUSTRATIONS',
               'INTRODUCTORY', 'COMPRISING', 'OF', 'MATERIALS', 'STORIES']

def printRoman(number):
    roman_num = ''
    num = [1, 4, 5, 9, 10, 40, 50, 90,
        100, 400, 500, 900, 1000]
    sym = ["I", "IV", "V", "IX", "X", "XL",
        "L", "XC", "C", "CD", "D", "CM", "M"]
    i = 12
     
    while number:
        div = number // num[i]
        number %= num[i]
 
        while div:
            roman_num += sym[i]
            div -= 1
        i -= 1
    
    return roman_num

num = []
num_word = []
cap_roman = []
roman_num = []
roman_book = []
cap_roman_book = []
prop_roman = []
num_only = []
roman_fullstop = []
roman_only = []
roman_chap_fullstop = []
num_fullstop = []
roman_only_space = []
roman_short = []
regex = ['\n[A-Z ]+[.]\r\n', 'Chapter \d+|CHAPTER \d+|Chapters \d+|CHAPTER [IVXLCDMivxlcdm]+|Chapter [IVXLCDMivxlcdm]+|Book [IVXLC]+|BOOK [IVXLC]+']


for i in range(1, 100):
    num.append('\nChapter ' + str(i))
    num_word.append('\nChapter ' + num2words(i).capitalize())
    roman_num.append('\nChapter ' + printRoman(i))
    cap_roman.append('\nCHAPTER ' + printRoman(i))
    roman_book.append('\nBook ' + printRoman(i))
    cap_roman_book.append('\nBOOK ' + printRoman(i))
    prop_roman.append('\nPROP. ' + printRoman(i) + '[.]')
    num_only.append('\n' + str(i) + '\r\n\r\n')
    roman_fullstop.append('\r\n' + printRoman(i) + '[.] ')
    roman_only.append('\n' + printRoman(i) + '\r\n')
    roman_chap_fullstop.append('\nCHAPTER. ' + printRoman(i) + '[.]')
    roman_only_space.append('\r\n' + printRoman(i) + '\r\n')
    num_fullstop.append('\r\n' + str(i) + '[.]')
    roman_short.append('  CHAP.   ' + printRoman(i) + '[.]\r\n')
    
header_list = num + num_word + cap_roman + roman_num + roman_book + cap_roman_book + prop_roman + num_only + roman_fullstop + roman_only + roman_chap_fullstop + num_fullstop + roman_only_space + roman_short
header = "|".join(header_list)

def remove_end(text, last_line):
    end = text.find(last_line)
    if (end > 0):
        text = text[:end + len(last_line)]
    return text



def chapIndexes(text):
    chap_index = []
    indexes = [
        match.start() for match in re.finditer(header, text)
    ]
   
    if(len(indexes) > 1):
        for i in range(len(indexes)-1):
            if (indexes[i+1] - indexes[i]) > 1500:
                chap_index.append(indexes[i])

        chap_index.append(indexes[-1])
        
    elif (len(indexes) == 1):
        chap_index.append(indexes[0])
        
    if len(chap_index) == 0:
        chap_index = chapIndexesbyCapWord(text)
    
    return chap_index

def chapIndexesbyCapWord(text):
    chap_index = []
    indexes = [
        match.start() for match in re.finditer(regex[0], text)
    ]
    if(len(indexes) > 1):
        for i in range(len(indexes)-1):
            if (indexes[i+1] - indexes[i]) > 1500:
                chap_index.append(indexes[i])   
    
    elif (len(indexes) == 1):
        chap_index.append(indexes[0])
    return chap_index

def splitbyChapters(text, chap_index):
    split_text = []
    
    if (len(chap_index) > 1):
        for i in range(len(chap_index) - 1):
            split_text.append(text[chap_index[i]:chap_index[i + 1]])
        return split_text
    elif (len(chap_index) == 1):
        split_text.append(text[chap_index[0]:])
        return split_text
    return text

def directory(input_name):
    dir = input_name #+ ' ' + datetime.now().strftime("Day-%d %m %y_Time-%H %M %S")
    if os.path.exists(dir):
        shutil.rmtree(dir)
    os.makedirs(dir)
    return dir

def saveChapters(dir, split_text, id): 
    # dir: test_data/Chapters3
    # split_text: list of chapters
    # id: 31671
    dir = directory(dir)
    folder = os.path.join(dir,id)
    os.mkdir(folder)
    chapter_list = []
    for i in split_text:
        if i != '':
            name = i.split("\r\n")
            name = [x for x in name if x != '']
            form_name = name[0].replace(".", "_").replace(" ", "_").replace(":", "").replace("?", "").replace('"', "").replace('\x00', "")
            form_name = form_name.strip()
            if(form_name not in remove_list):
                with open (f'./{folder}/{form_name}.txt', "w", encoding='utf-8') as f:
                    f.write(i)
                    f.close()
                    chapter_list.append(form_name)
    return chapter_list

def savecleanBooks(text, id):
    folder = 'cleaned_text'
    if(not path.exists("cleaned_text")):
        os.mkdir(folder)
    with open (f'./{folder}/{id}.txt', "w", encoding='utf-8') as f:
        f.write(text)
        f.close()

######################################################################################################

def make_bigrams(bigram_mod, texts):
    bigram = [bigram_mod[doc] for doc in texts]
    docs_stop = [[w for w in doc if w not in stop_list] for doc in bigram] 
    bigram_cleaned = [[w for w in doc if len(w)>3] for doc in docs_stop]
    return bigram_cleaned

def make_trigrams(bigram_mod, trigram_mod, texts):
    trigram = [trigram_mod[bigram_mod[doc]] for doc in texts]
    docs_stop = [[w for w in doc if w not in stop_list] for doc in trigram] 
    trigram_cleaned = [[w for w in doc if len(w)>3] for doc in docs_stop]
    return trigram_cleaned
######################################################################################################
# Summarisation
from nltk.cluster.util import cosine_distance
import numpy as np


def splitbySentences(books_directory, selected_chap):
    # Create a list to store the text data of each book
    book_texts = []
    chapters_name = []

    # Loop through each file in the directory
    for filename in os.listdir(books_directory):
        if filename.endswith('.txt'):
            with open(os.path.join(books_directory, filename), "r", encoding="utf8", errors='ignore') as file:
                book_text = file.read()
                book_texts.append(book_text)
                chapters_name.append(filename.replace('.txt',''))
    
    selected_chap_index = chapters_name.index(selected_chap)

    sentences = nltk.sent_tokenize(book_texts[selected_chap_index])
    book_sentences = []
    for sen in sentences:
        cleaned_sen = sen.replace("\n", " ")
        book_sentences.append(cleaned_sen.split(" "))
    new_sentences = [[x for x in sentence if x] for sentence in book_sentences]
    return new_sentences

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

def build_similarity_matrix(sentences, stop_words):
    # Create an empty similarity matrix
    similarity_matrix = np.zeros((len(sentences), len(sentences)))
 
    for idx1 in range(len(sentences)):
        for idx2 in range(len(sentences)):
            if idx1 == idx2: #ignore if both are same sentences
                continue 
            similarity_matrix[idx1][idx2] = sentence_similarity(sentences[idx1], sentences[idx2], stop_words)
    return similarity_matrix
