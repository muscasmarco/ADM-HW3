#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:39:43 2019

@author: marco
"""

from nltk.tokenize import RegexpTokenizer
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords

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
    