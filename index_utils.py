#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:39:43 2019

@author: marco
"""

from nltk.tokenize import RegexpTokenizer
from nltk.stem import LancasterStemmer
from nltk.corpus import stopwords
import pandas as pd

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
    
def count_words_dataset():
    
    print('Building dataset for counting words in document...')
    dataset_raw = pd.read_csv('./dataset/film_info_dataset.tsv', sep='\t')
    dataset_raw = dataset_raw.drop(columns='Unnamed: 0')
    cols = ['document_id', 'num_words']
    doc_num_words = pd.DataFrame(columns=cols)
    for doc_id in dataset_raw.index:
        
        if doc_id % 100 == 0:
            print('  ', doc_id/len(dataset_raw)*100, '%')
        
        num_words = 0
        
        num_words += len(preprocess(dataset_raw['title'][doc_id]))
        num_words += len(preprocess(dataset_raw['intro'][doc_id]))
        num_words += len(preprocess(dataset_raw['plot'][doc_id]))
        num_words += len(preprocess(dataset_raw['film_name'][doc_id]))
        num_words += len(preprocess(dataset_raw['director'][doc_id]))
        num_words += len(preprocess(dataset_raw['producer'][doc_id]))
        num_words += len(preprocess(dataset_raw['writer'][doc_id]))
        num_words += len(preprocess(dataset_raw['starring'][doc_id]))
        num_words += len(preprocess(dataset_raw['music'][doc_id]))
        num_words += len(preprocess(dataset_raw['release_date'][doc_id]))
        num_words += len(preprocess(dataset_raw['runtime'][doc_id]))
        num_words += len(preprocess(dataset_raw['country'][doc_id]))
        num_words += len(preprocess(dataset_raw['language'][doc_id]))
        num_words += len(preprocess(dataset_raw['budget'][doc_id]))
        
        row = pd.DataFrame([[doc_id, num_words]], columns=cols)
        doc_num_words = doc_num_words.append(row, ignore_index=True)        
        
    dataset_csv_separator = '\t' # Separator between columns in the file
    dataset_csv_na_rep = 'NA' # Default null value representation
    dataset_csv_path = './dataset/document_num_words.csv'
    doc_num_words.to_csv(path_or_buf=dataset_csv_path, sep=dataset_csv_separator, na_rep=dataset_csv_na_rep)    
    print('Done')