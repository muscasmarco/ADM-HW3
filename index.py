#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 13:48:45 2019

@author: marco
"""
import pandas as pd
from index_utils import preprocess

dataset_raw = pd.read_csv('./dataset/film_info_dataset.tsv', sep='\t')
dataset_raw = dataset_raw.drop(columns='Unnamed: 0')

# Initializing nltk lists to filter

inverted_index_tmp = dict()
print('Building the inverted index..')
for index in range(10000):
    
    terms = []
    
    terms.extend(preprocess(dataset_raw['title'][index]))
    terms.extend(preprocess(dataset_raw['intro'][index]))
    terms.extend(preprocess(dataset_raw['plot'][index]))
    
    # Comment from here
    
    terms.extend(preprocess(dataset_raw['film_name'][index]))
    terms.extend(preprocess(dataset_raw['director'][index]))
    terms.extend(preprocess(dataset_raw['producer'][index]))
    terms.extend(preprocess(dataset_raw['writer'][index]))
    terms.extend(preprocess(dataset_raw['starring'][index]))
    terms.extend(preprocess(dataset_raw['music'][index]))
    terms.extend(preprocess(dataset_raw['release_date'][index]))
    terms.extend(preprocess(dataset_raw['runtime'][index]))
    terms.extend(preprocess(dataset_raw['country'][index]))
    terms.extend(preprocess(dataset_raw['language'][index]))
    terms.extend(preprocess(dataset_raw['budget'][index]))
    
    # To here to get the title-intro-plot dictionaries
    
    
    # Removing duplicates
    #terms = list(dict.fromkeys(terms))
    for term in terms:
        if term != 'NA' or term != 'na':
            if term not in inverted_index_tmp.keys():
                inverted_index_tmp[term] = [index]
            else:
                inverted_index_tmp[term].append(index)

vocabulary_tmp = list(inverted_index_tmp.keys())

# Building the actual inverted index with the mappings
inverted_index = list()
vocabulary = list()

# Saving the vocabulary to file
for i, word in zip(range(len(vocabulary_tmp)), vocabulary_tmp):
    inverted_index.append([i, inverted_index_tmp[word]])
    vocabulary.append([i, word])
print('Done.')
''' Saving to file now '''
print('Saving CSVs to file...')
vocabulary_ds = pd.DataFrame(columns=['term_id','term'])
for vocab_id in range(len(vocabulary)):
    print(vocab_id/len(vocabulary) * 100, '%')
    vocabulary_ds = vocabulary_ds.append(pd.DataFrame([vocabulary[vocab_id]], columns=['term_id', 'term']), ignore_index=True)
vocabulary_ds.to_csv(path_or_buf='./dataset/term_dictionary.csv', sep='\t', na_rep='NA')

# Making inverted index into a DataFrame so it can be easily saved
inverted_index_ds = pd.DataFrame(columns=['term_id','document_id'])
for i in range(len(inverted_index)):
    print(i/len(inverted_index) * 100, '%')
    tup = inverted_index[i]
    row = pd.DataFrame([tup], columns=['term_id','document_id'])
    inverted_index_ds = inverted_index_ds.append(row, ignore_index=True)

dataset_csv_separator = '\t' # Separator between columns in the file
dataset_csv_na_rep = 'NA' # Default null value representation
dataset_csv_path = './dataset/inverted_index.csv'
inverted_index_ds.to_csv(path_or_buf=dataset_csv_path, sep=dataset_csv_separator, na_rep=dataset_csv_na_rep)    
print('Done.')    

    