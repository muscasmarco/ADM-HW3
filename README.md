# ADM-HW3

- Marco Muscas (Student ID: 1883544)

Work started on November 19th, ended November 24th.

## File structure

### main.py 
This contains all the functions used to run the different search engines. Each will first load the necessary datasets.
It also contains the function used to calculate the score for Part 3.

### collector.py 
This contains the code to download the Wikipedia pages an store them with a specific name.

### collector_utils.py 
Not needed.

### parser.py
This file contains the function used to parse each html file in the range 0.html to 9999.html. It also explains 
how the file were parsed.

### index.py

This file generates all the indexes needed for the various exercises. 

### index_utils.py

This file contains two functions. The first is there to create an additional index to easily retrieve the length
of a preprocessed document. The other one creates the inverted index with tfidf for each document.

### utils.py

This contains the function 'preprocess' which is used throughout the whole project. It allows a raw string to be 
tokenized and have stopwords and punctuation removed.

### exercise_4.py

Solution for exercise 4. More on how it works in the file itself. 
