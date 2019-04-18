#!/usr/bin/env python
# coding: utf-8

# # IST 652 Lab #6
# ### Instructions
# - Complete all 6 questions in this assignment.
# - You may work with others, <b> but the work you submit must be your own </b>. You can differentiate your work by adding comments or changing the values you use to test your code. However, submitting some else's work as your own is an academic integrity violation and will be raised to academic affairs.
# - It is always better to attempt a problem as partial credit may be granted.
# 
# 
# ### Submission Guide:
# - Submit your answers on BlackBoard by Thursday 2019-04-18.
# - The file must be either a .py or .ipynb file type.
# - <i><span style="color:red">The name of the file you submit should be <i><b> ist652_lab6_lastname.py (.ipynb) </i></b>.</span>
# 
# 
# 
# ### Grading [ 6 total points ]
# For Each Questions (1-6), the following credit will be awarded:
# - 0.75 for printing the correct answer to the console.
# - 0.15 for approaching the problem efficiently.
# - 0.05 for properly documenting and commenting your code.
# 

# ---
# ## Questions

# ---

# #### First, download the Watson_Tweets.csv from BlackBoard. 
# #### ( 1 ) Load the Watson_Tweets.csv file using pandas pd.read_csv() method and describe the data set.
# - NOTE: The file is pipe (|) seperated.
#  - use the method parameter `sep` to properly parse and read the pipe-delimeted file
# 
# ##### [1 point]

# In[33]:


# Enter your code here, printing relevant answers to console:
import pandas as pd

data = pd.read_csv('/Users/jenyeulo/Documents/Syracuse_University/IST652/watson_tweets.csv', sep = '|')
data.describe()


# ---
# #### ( 2 ) Tokenize the <u>dataframe</u> of tweets into a <u>list</u> of lowercase tokens using the NLTK TweetTokenizer method. Print the number of tokens.
# 
# - Consider the method series.tolist() to convert the dataframe to a list.
# - NOTE: The expected object for analysis is a list of tokens, so carefully apply the tokenizer to the original list of tweets.
# 
# ##### [1 point]

# In[48]:


# Enter your code here, printing relevant answers to console:
import nltk
from nltk.tokenize import TweetTokenizer

datalist = data["tweets"].tolist() #convert the dataframe into a list
datalist = [x.lower() for x in datalist] #make the list lowercase

#tknzr = TweetTokenizer()
#tknzr.tokenize(datalist)

all_tokens = [tok for tweet in datalist for tok in nltk.word_tokenize(tweet)]
len(all_tokens)

#tokens = nltk.word_tokenize(datalist)
#type(datalist)
all_tokens[:20]


#  ----

# #### alpha_filter

# In[51]:


# function that takes a word and returns true if it consists only
#   of non-alphabetic characters
import re

def alpha_filter(w):
    # pattern to match a word of non-alphabetical characters
    pattern = re.compile('^[^a-z]+$')
    if (pattern.match(w)):
        return True
    else:
        return False


# #### ( 3 ) Run the above code block which creates the alpha_filter function. Then, in your own words, describe what the regex query is filtering for.
# 
# ##### [1 point]
# 
# #### Enter your answer here,<u>in english, not python:</u>

# In[ ]:


# It is a function that takes a word and returns true if it consists only of non-alphabetic characters


# ----

# #### ( 4 ) Return a new list of tokens filtered by  the alpha_filter function and without StopWords.
# - Recall the stopwords list from NTLK which we covered in class:
#     - `nltk.corpus.stopwords.words('english')`
# 
# ##### [1 point]

# In[52]:


# Enter your code here, printing relevant answers to console:
nltk_stopwords = nltk.corpus.stopwords.words('english')
all_stopped_tokens = [tok for tok in all_tokens if not tok in nltk_stopwords] #removes stopwords


token_list = [tok for tok in all_stopped_tokens if not alpha_filter(tok)] # remove words with all non-alphabetic characters

token_list[:20]


# ----

# #### ( 5 ) Apply the frequency distribution to your list from question (4) and print the 50 most common tokens.
# - Note: recall the `nltk.FreqDist` method
# 
# ##### [1 point]

# In[53]:


# Enter your code here, printing relevant answers to console:
msgFD = nltk.FreqDist(token_list)
top_words = msgFD.most_common(30)
for word, freq in top_words:
    print(word, freq)


# ---
# #### ( 6 ) Return the top 25 bigrams by applying a bigram frequency analysis of the tokens found in ( 4 ).
# Note: Use the ntlk methods:
# - `BigramCollocationFinder.from_words()`
# - `score_ngrams()`
# 
# ##### [1 point]

# In[55]:


# Enter your code here, printing relevant answers to console:
from nltk.collocations import *
bigram_measures = nltk.collocations.BigramAssocMeasures()

finder = BigramCollocationFinder.from_words(token_list)
scored = finder.score_ngrams(bigram_measures.raw_freq)
scored[:25]


# ---
