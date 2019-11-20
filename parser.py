#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 23:19:41 2019

@author: marco
"""
from bs4 import BeautifulSoup
import pandas as pd
import os

def join_list_strings(list_strings):
    res = ''
    for string in list_strings:
        res = res + ''.join(string)
    return res

pages_root_path = './wiki-pages'

cols = ['title','intro','plot', 'film_name', 'director', 'producer',
           'writer', 'starring', 'music', 'release_date', 'runtime',
           'country', 'language', 'budget']

ds = pd.DataFrame(columns=cols)

for i in range(10001):
    html_path = str('%s/%d.html' %(pages_root_path, i))
    
    if os.path.exists(html_path):
        soup = BeautifulSoup(open(html_path),'html.parser')
        title = ''
        intro = ''
        plot = ''
        director = ''
        producer = ''
        writer = ''
        starring = ''
        music = ''
        release_date = ''
        runtime = ''
        country = ''
        language = ''
        budget = ''
        
        try:
            title = soup.find('h1',{'id':'firstHeading'}).text
            
            paragraphs = [x.text.split('\n') for x in soup.findAll('p')]
            
            intro = ''.join(paragraphs[0])
            
            # Multiple joins required
            plot = [''.join(subpar) for subpar in paragraphs[1:]]
            plot = join_list_strings(plot)
            
            # Now getting the info box, the result will be a list of
            # table rows
            tr = soup.find('table', {'class':'infobox vevent'}).findAll('tr')
            
            
            for r in tr:
                tr_soup = BeautifulSoup(r.text, 'html.parser')
                
                # Each prefix (i.e. Directed by) will act as a separator
                # between the name of the attribute and the value.
                # Since values could be on one or more lines, I supposed that
                # all values (on different lines) are about the same attribute
                
                if 'Directed by' in r.text:
                    director = ''.join(r.text.split('Directed by')[1:])
                
                if 'Distributed by' in r.text:
                    producer = ''.join(r.text.split('Distributed by')[1:])
                
                if 'Written by' in r.text:
                    writer = ''.join(r.text.split('Written by')[1:])
                    
                if 'Starring' in r.text:
                    starring = ' '.join(r.text.split('Starring')[1:])
                
                if 'Music by' in r.text:
                    music = ' '.join(r.text.split('Music by')[1:])
                
                if 'Release date' in r.text:
                    release_date = ' '.join(r.text.split('Release date')[1:])
                
                if 'Running time' in r.text:
                    runtime =  ' '.join(r.text.split('Running time')[1:])
                    
                if 'Country' in r.text:
                    country = ' '.join(r.text.split('Country')[1:])
                
                if 'Language' in r.text:
                    language = ' '.join(r.text.split('Language')[1:])
                    
                if 'Budget' in r.text:
                    budget = ' '.join(r.text.split('Budget')[1:])
                    
        except:
            print('%d.html | This film does not have an infobox.' % i)
            pass
        
        # Now let's insert all the data in the dataset
        
        new_row = pd.DataFrame([[title, intro, plot, title, director, producer, writer, starring,
                                music, release_date, runtime, country, language, budget]], columns=cols)
                
        ds = ds.append(new_row, ignore_index=True)
                
# Data can be now written on the .tsv file
        
dataset_tsv_separator = '\t' # Separator between columns in the file
dataset_tsv_na_rep = 'NA' # Default null value representation
dataset_tsv_path = './dataset/film_info_dataset.tsv'
ds.to_csv(path_or_buf=dataset_tsv_path, sep=dataset_tsv_separator, na_rep=dataset_tsv_na_rep)    
                
                
                
                
                
        