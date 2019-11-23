#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:31:02 2019

@author: marco
"""
from index_utils import preprocess
import pandas as pd
import numpy as np
'''
def use_search_engine_one():
    
    print('Loading datasets...')
    vocabulary = pd.read_csv('./dataset/term_dictionary_intro_plot.csv', sep='\t')
    inverted_index = pd.read_csv('./dataset/inverted_index_intro_plot.csv', sep='\t')
    film_ds = pd.read_csv('./dataset/film_info_dataset.tsv', sep='\t')
    print('Done.')
    
    query = input("Insert your query: ")
    
    query_terms = preprocess(query)
    vocab_ids = []
    for query_term in query_terms:
        term_ids_res = vocabulary.term_id[vocabulary.term == query_term]
        
        if len(term_ids_res.values) > 0:
            vocab_ids.append(term_ids_res.values[0])
    pages = {}
    
    for vocab_id in vocab_ids:
        pages_as_str = inverted_index.document_id[inverted_index.term_id == vocab_id].values[0]
        pages_for_single_term = list(eval(pages_as_str))
        
        for page_id in pages_for_single_term:
            if page_id not in pages.keys():
                pages[page_id] = 1
            else:
                pages[page_id] += 1
                
    results = [page_id for page_id in pages.keys() if pages[page_id] == len(vocab_ids)]
    
    
    if len(results) > 0:
        for page_id in results:
            row = film_ds[film_ds.index == page_id]
            
            title = row['title'].values[0]
            
            print(title)
    else: 
        print('No results for your search! :(')
'''
def compute_tfidf(term_id, document_id, inverted_index_dict_with_duplicates, inverted_index_dict_no_duplicates, num_words):
    
    num_occurrences = len(inverted_index_dict_no_duplicates[term_id])
    
    num_document_occurrences = len(inverted_index_dict_no_duplicates[term_id])

    tf = num_occurrences/num_words
    idf = np.log(10000/num_document_occurrences)
    
    tfidf = tf * idf
    
    return tfidf
            
''' Search engine 2 '''

''' Datasets 2 '''

''' Loading the datasets '''
vocabulary = pd.read_csv('./dataset/term_dictionary.csv', sep='\t')
inverted_index_ds = pd.read_csv('./dataset/inverted_index.csv', sep='\t')
film_info = pd.read_csv('./dataset/film_info_dataset.tsv', sep='\t')
num_words_dataset = pd.read_csv('./dataset/document_num_words.csv', sep='\t')
''' Dropping Unnamed: 0 columns as it is not necessary '''

vocabulary = vocabulary.drop('Unnamed: 0', axis=1)
inverted_index_ds = inverted_index_ds.drop('Unnamed: 0', axis=1)
film_info = film_info.drop('Unnamed: 0', axis=1)
num_words_dataset = num_words_dataset.drop('Unnamed: 0', axis=1)


''' Converting dataframe into other data structures to optimize 
    running time '''
inverted_index_dict = inverted_index_ds.to_dict()['document_id']   
inverted_index_dict_with_duplicates = {key:list(eval(inverted_index_dict[key])) for key in inverted_index_dict.keys()}
inverted_index_dict_no_duplicates = {key:list(dict.fromkeys(inverted_index_dict_with_duplicates[key])) for key in inverted_index_dict_with_duplicates.keys()}
num_words_dict = num_words_dataset.to_dict()['num_words']



cols = ['term_id', 'document_info']
tfidf_dataset = pd.DataFrame(columns=cols)

for term_id in inverted_index_dict.keys():
    
    if term_id % 100 == 0:
        print(term_id/len(inverted_index_dict.keys()) * 100, '%')
    
    documents = inverted_index_dict_no_duplicates[term_id]
    
    data_list = []
    
    for doc_id in documents:
        tfidf_score = compute_tfidf(term_id, doc_id, inverted_index_dict_with_duplicates, inverted_index_dict_no_duplicates, num_words_dict[doc_id])
        document_data = (doc_id, tfidf_score)
        data_list.append(document_data)
        
    tfidf_dataset = tfidf_dataset.append(pd.DataFrame([[term_id, data_list]], columns=cols), sort=False)




dataset_csv_separator = '\t' # Separator between columns in the file
dataset_csv_na_rep = 'NA' # Default null value representation
dataset_csv_path = './dataset/tfidf_inverted_index.csv'
tfidf_dataset.to_csv(path_or_buf=dataset_csv_path, sep=dataset_csv_separator, na_rep=dataset_csv_na_rep)    



















































