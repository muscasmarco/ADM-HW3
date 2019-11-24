#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 17:59:23 2019

@author: marco
"""
from nltk.tokenize import RegexpTokenizer
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords

''' The preprocess function uses some tools from the nltk library to tokenize
    a raw string, so that each token is not a stop word and stemmed. '''
def preprocess(raw_string):
    stop_words = set(stopwords.words('english')) 
    res = ''
    if raw_string != 'NA':
        res = str(raw_string).lower().split()
        
        # Remove stopwords
        res = [word for word in res if word not in stop_words]
        
        # Remove punctuation
        tokenizer = RegexpTokenizer(r'\w+')

        tmp_res = []
        for s in res:
            tokens = tokenizer.tokenize(s)
            tmp_res.extend(tokens)
        res = tmp_res
        
        
        # Stemming
        stemmer = LancasterStemmer()
        tmp_res = []
        for s in res:
            if s.isalpha():
                tmp_res.append(stemmer.stem(s))
            else:
                tmp_res.append(s)
        res = tmp_res
        
    else:
        res = ['NA']
        
    return res