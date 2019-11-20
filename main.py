#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:31:02 2019

@author: marco
"""
from index_utils import preprocess
import pandas as pd


print('Loading datasets...')
vocabulary = pd.read_csv('./dataset/term_dictionary_intro_plot.csv', sep='\t')
inverted_index = pd.read_csv('./dataset/inverted_index_intro_plot.csv', sep='\t')
film_ds = pd.read_csv('./dataset/film_info_dataset.tsv', sep='\t')
print('Done.')


def use_search_engine_one(query):

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
        
