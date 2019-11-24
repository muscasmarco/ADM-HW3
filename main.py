#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 20:31:02 2019

@author: marco
"""
from index_utils import preprocess
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from numpy.linalg import norm

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

def compute_tfidf(term_id, document_id, inverted_index_dict_with_duplicates, inverted_index_dict_no_duplicates, num_words):
    
    num_occurrences = len(inverted_index_dict_no_duplicates[term_id])
    
    num_document_occurrences = len(inverted_index_dict_no_duplicates[term_id])

    tf = num_occurrences/num_words
    idf = np.log(10000/num_document_occurrences)
    
    tfidf = tf * idf
    
    return tfidf
            
''' Search engine 2 '''

''' Datasets 2 '''

def compute_cosine_similarities(query_elements):
    
    print('Computing cosine similarities.')
    print('Loading datasets')
    
    vocabulary = pd.read_csv('./dataset/term_dictionary.csv', sep='\t')
    tfidf_index = pd.read_csv('./dataset/tfidf_inverted_index.csv', sep='\t')
    vocabulary = vocabulary.drop('Unnamed: 0', axis=1)
    tfidf_index = tfidf_index.drop('Unnamed: 0', axis=1)
    print('Loading datasets done.')
    
    # Compute tfidf for the query elements
    query_len = len(query_elements)
    query_scores = []
    
    documents = []
    # Calculating tf-idf score with respect to the query
    for word in query_elements:
        if word in vocabulary['term'].values:      
            word_id = vocabulary.term_id[vocabulary.term == word].values[0] # First, find the term_id
            word_occurrences = query_elements.count(word) # Number of distinct instances of same term in query
            docs_containing_term = tfidf_index.document_info[tfidf_index.term_id == word_id].values[0] 
            documents.append(docs_containing_term) # It will be useful in the next step
            tf = word_occurrences/query_len    
            idf = np.log(10000/len(docs_containing_term))         
            tfidf = tf * idf
            query_scores.append([word_id,tfidf])
        else:
            query_scores.append([word_id,0])
    
    # Creating the tfidf for each term containing (or not) each term in the query
    docs_scores = {}
    for i in range(len(query_scores)):
        term_id = query_scores[i][0]
        
        for document in list(eval(tfidf_index.document_info[tfidf_index.term_id == term_id].values[0])):
            document_id = document[0]
            # Initialize score vector
            if document_id not in docs_scores.keys():
                docs_scores[document_id] = np.zeros(query_len)
            
            docs_scores[document_id][i] = document[1] # Registering the tfidf of the document
        
        
    resulting_docs = []
    # Compute the cosine similarity for each combination query_score, document_score:
    for key in docs_scores.keys():
        query_score = [qs[1] for qs in query_scores]
        doc_score = docs_scores[key]
        
        dot_prod = np.dot(query_score, doc_score)
        norm_prod = np.linalg.norm(query_score,ord=2) * np.linalg.norm(doc_score, ord=2)
        cos_similiarity = abs(dot_prod/norm_prod)
        resulting_docs.append([key, cos_similiarity])
 
    resulting_docs.sort(key=lambda x:x[1], reverse=False)
    
    return resulting_docs


#def use_search_engine_two():
    
''' Loading datasets '''

def use_search_engine_two():

    film_ds = pd.read_csv('./dataset/film_info_dataset.tsv', sep='\t')
    film_ds = film_ds.drop('Unnamed: 0', axis=1)
    
    query_terms = preprocess(str(input('Insert your query: ')))
    scores = compute_cosine_similarities(query_terms)
    
    for score in scores[:10]:
        doc_id = score[0]
        
        title = film_ds.title[film_ds.index == doc_id].values[0]
        director = film_ds.director[film_ds.index == doc_id].values[0]
        print(doc_id,' ', title, ' ', director)
    
     
    
    
    































