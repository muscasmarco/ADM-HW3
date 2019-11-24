#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:39:43 2019

@author: marco
"""


import pandas as pd
from index import compute_tfidf
from utils import preprocess

    
''' This is an auxiliary index file used when calculating the tf-idf. As it 
    requires the length of the analyzed text (which is an expensive operation). '''
    
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
    
''' This function is used to create the index like term_id:[ (doc_1, tf-idf1), ...] '''

def create_tfidf_dataset():
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
    
