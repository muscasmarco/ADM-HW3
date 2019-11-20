#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 19 22:43:43 2019

@author: marco
"""
from bs4 import BeautifulSoup
import time
import random
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

urls_file_path = '/home/marco/workspace/git/ADM-HW3/wiki-urls/movies1.html'
urls_file = open(urls_file_path, 'r')
soup = BeautifulSoup(urls_file, 'html.parser')

urls = [tag['href'] for tag in soup.findAll('a', href=True)]

http = urllib3.PoolManager()

for i in range(len(urls)):
    url = urls[i]
    
    try:
        response = http.request('GET', url)
        content = response.data.decode('utf-8')
        
        f = open(str('./wiki-pages/%d.html' % i), 'w')
        f.write(str(content))
        f.close()
    
        wait_time = random.randint(1, 4)
        time.sleep(wait_time)
    except Exception as e:
        print(e)
        time.sleep(60 * 20)
