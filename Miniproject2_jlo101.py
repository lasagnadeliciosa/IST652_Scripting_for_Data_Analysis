#!/usr/bin/env python
# coding: utf-8

# In[134]:


import tweepy
import json
import yaml
import pandas as pd
import pymongo
import nltk
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt


# In[136]:


#Specify how many pages of tweets we are importing (each page is 200 tweets)
pages_to_query = 5
q1_words = 50
q2_words = 30
q3_words = None



# In[137]:


# function that takes a word and returns true if it consists only of non-alphabetic characters
def alpha_filter(w):
    # pattern to match a word of non-alphabetical characters
    pattern = re.compile('^[^a-z]+$')
    if (pattern.match(w)):
        return True
    else:
        return False 

#function that tokenizes and removes stopwords from list
def text_clean(list_of_strings):
    #tokenization
    all_tokens = [tok.lower() for string in list_of_strings for tok in nltk.word_tokenize(string)]
    #remove stopwords
    nltk_stopwords = nltk.corpus.stopwords.words('english')
    all_stopped_tokens = [tok for tok in all_tokens if not tok in nltk_stopwords]
    token_list = [tok for tok in all_stopped_tokens if not alpha_filter(tok)]
    return token_list

#function that performs NLP analysis on a list of strings
def nlp_analysis(token_list, num_of_words):
    #Final step, count the frequency of the tokens and interpret the meaning.
    msgFD = nltk.FreqDist(token_list)
    top_words = msgFD.most_common(num_of_words)
    return top_words

#generate a world cloud and saves as PNG
def generate_wc(cleaned_words, file_name):
    # Create a list of word
    cyber_space_joined_top100_words = ' '.join(cleaned_words)
    # Create the wordcloud object
    cyber_wordcloud = WordCloud(background_color = 'black',width = 1600, height = 1600, margin = 0).generate(cyber_space_joined_top100_words)
    # Display the generated image and save image as PNG:
    plt.imshow(cyber_wordcloud, interpolation = 'gaussian')
    plt.axis("off")
    plt.margins(x = 1, y = 1)
    plt.show()
    cyber_wordcloud.to_file(file_name + '.png')


# In[138]:


#creating a database
client = pymongo.MongoClient()
client.database_names()

#create a new db called cyber_tweets
db = client.cyber_db

#create a new collection(a group of documents) called deltatweets
cyber_timeline = db.cyber_tweets
cyber_timeline.drop() # drop all existing data, just to refresh the table as new tweets comes in in the future


# In[139]:


#login to twitter API
auth = tweepy.OAuthHandler(config['CONSUMER_KEY'],config['CONSUMER_SECRET'])
auth.set_access_token(config['OAUTH_TOKEN'],config['OAUTH_SECRET'])
api = tweepy.API(auth)


# In[140]:


#insert 4 pages worth of tweets into cyber_tweets collection

for i in range(1, pages_to_query+1):
    #use API to scrape CyberpunkGame's tweets and all information related to the tweets
    timeline = api.user_timeline('CyberpunkGame', count=200, page=i)

    #convert the data(tweepy.models.ResultSet) into a python list of tweets
    tweet_list = list(timeline)

    #use list comprehension to extract json field of the tweets
    tweet_json = [tweet._json for tweet in tweet_list]

    #store json tweets into cyber_db's cyber_tweets collection
    cyber_timeline.insert_many(tweet_json)


# In[175]:


#query data from cyber_db and convert it into a list of dictionaries
cyber_docs = list(cyber_timeline.find())
#cyber_docs[123] #use this for testing


# In[142]:


#Question 1: Word cloud for the top 100 most favorited tweets
cyber_df1 = pd.DataFrame(cyber_docs)

cyber_df1_sorted = cyber_df1.sort_values(by=['favorite_count'], ascending=False) #sort by descending favorite_count


# In[171]:


cyber_top100fav = cyber_df1_sorted.to_dict('records')[:100] #convert pd dataframe back to a list of dictionaries
#to_dict('records') is a syntax, keep columns as keys, and values as values
#cyber_top100fav[:1]


# In[176]:


#Takes the top 100 tweet's 'text' field and store into a list of strings.
cyber_top100_texts = [tweet['text'] for tweet in cyber_top100fav if 'text' in tweet.keys()]

#Top 100 favorite tweet's top 30 words by frequency

cyber_top100_words = text_clean(cyber_top100_texts)
#cyber_top100_words

generate_wc(cyber_top100_words, 'cyberWC_top100')


# In[89]:


#Question 2: Analyze tokens from Jan to April.
#create for loop to categorize tweets by months.
cyber_jan2019_tweets = []
cyber_feb2019_tweets = []
cyber_mar2019_tweets = []
cyber_apr2019_tweets = []

for doc in cyber_docs:
    date = doc['created_at'].split()
    if date[1] == 'Jan' and date[-1] == '2019':
        cyber_jan2019_tweets.append(doc)
    if date[1] == 'Feb' and date[-1] == '2019':
        cyber_feb2019_tweets.append(doc)
    if date[1] == 'Mar' and date[-1] == '2019':
        cyber_mar2019_tweets.append(doc)
    if date[1] == 'Apr' and date[-1] == '2019':
        cyber_apr2019_tweets.append(doc)


# In[129]:


#extract the tweet texts from each month
cyber_jan2019_texts = [tweet['text'] for tweet in cyber_jan2019_tweets if 'text' in tweet.keys()]
cyber_feb2019_texts = [tweet['text'] for tweet in cyber_feb2019_tweets if 'text' in tweet.keys()]
cyber_mar2019_texts = [tweet['text'] for tweet in cyber_mar2019_tweets if 'text' in tweet.keys()]
cyber_apr2019_texts = [tweet['text'] for tweet in cyber_apr2019_tweets if 'text' in tweet.keys()]

cyber_jan2019_texts = text_clean(cyber_jan2019_texts)
cyber_feb2019_texts = text_clean(cyber_feb2019_texts)
cyber_mar2019_texts = text_clean(cyber_mar2019_texts)
cyber_apr2019_texts = text_clean(cyber_apr2019_texts)
#note, you can feed the above 4 variables to create wordcloud


# In[131]:


#conduct NLP analysis on all four months
cyber_jan2019_nlp = nlp_analysis(cyber_jan2019_texts, q2_words)
cyber_feb2019_nlp = nlp_analysis(cyber_feb2019_texts, q2_words)
cyber_mar2019_nlp = nlp_analysis(cyber_mar2019_texts, q2_words)
cyber_apr2019_nlp = nlp_analysis(cyber_apr2019_texts, q2_words)


# In[163]:


cyber_4month_word_counts = {}

for word, count in cyber_jan2019_nlp:
    cyber_4month_word_counts[word] = [count,0,0,0]
    
for word, count in cyber_feb2019_nlp:
    if word in cyber_4month_word_counts:
        cyber_4month_word_counts[word][1] = count
    else:    
        cyber_4month_word_counts[word] = [0,count,0,0]
        
for word, count in cyber_mar2019_nlp:
    if word in cyber_4month_word_counts:
        cyber_4month_word_counts[word][2] = count
    else:    
        cyber_4month_word_counts[word] = [0,0,count,0]
        
for word, count in cyber_apr2019_nlp:
    if word in cyber_4month_word_counts:
        cyber_4month_word_counts[word][3] = count
    else:    
        cyber_4month_word_counts[word] = [0,0,0,count]
        
cyber_df2 = pd.DataFrame.from_dict(cyber_4month_word_counts, orient='index', columns=['Jan', 'Feb', 'Mar', 'Apr'])

cyber_df2

#export it later


# In[164]:


#Question 3
#create a new collection for mnb_tweets
mnb_timeline = db.mnb_tweets
mnb_timeline.drop() # drop all existing data, just to refresh the table as new tweets comes in in the future


# In[165]:


#insert 4 pages worth of tweets into mnb_tweets collection

for i in range(1, pages_to_query+1):
    #use API to scrape CyberpunkGame's tweets and all information related to the tweets
    timeline = api.user_timeline('Mount_and_Blade', count=200, page=i)

    #convert the data(tweepy.models.ResultSet) into a python list of tweets
    tweet_list = list(timeline)

    #use list comprehension to extract json field of the tweets
    tweet_json = [tweet._json for tweet in tweet_list]

    #store json tweets into cyber_db's cyber_tweets collection
    mnb_timeline.insert_many(tweet_json)


# In[178]:


#query data from cyber_db and convert it into a list of dictionaries
mnb_docs = list(mnb_timeline.find())
#docs[123] #use this for testing

#extract tweet text from dictionary from both database
cyber_texts = [tweet['text'] for tweet in cyber_docs if 'text' in tweet.keys()]
mnb_texts = [tweet['text'] for tweet in mnb_docs if 'text' in tweet.keys()]

#clean both texts
cyber_words = text_clean(cyber_texts)
mnb_words = text_clean(mnb_texts)

#conduct NLP analysis, it is a list of tuple
cyber_nlp = nlp_analysis(cyber_words, None)
mnb_nlp = nlp_analysis(mnb_words, None) 


# In[195]:


cyber_mnb_inner_join = {}

cyber_nlp_map = dict(cyber_nlp)

for word, count in mnb_nlp:
    if word in cyber_nlp_map:
        cyber_mnb_inner_join[word] = [cyber_nlp_map[word], count]
        
cyber_mnb_inner_join

cyber_mnb_df = pd.DataFrame.from_dict(cyber_mnb_inner_join, orient='index', columns=['CyberPunk2077', 'Mount & Blade'])

cyber_mnb_df['cyber+mnb'] = cyber_mnb_df['CyberPunk2077'] + cyber_mnb_df['Mount & Blade']

cyber_mnb_df_sorted = cyber_mnb_df.sort_values(by=['cyber+mnb'], ascending=False)

cyber_mnb_df_sorted[:100].to_csv('cyber+mnb_common_words')


# In[ ]:


#notes:
[
    ('http', 27, 38, 29, 11), 
    ...
]

[
    {
        word: 'http',
        jan: 27,
        feb: 38,
        mar:29
        ...
    },
    ...
]


{
    http: [27, 38, 29, 11],
    alexwolfcosplay: [11, ?, ?, ?],
    ...
}

{
    http: {Jan:27, Feb:38, Mar:29, Apr:11},
    alexwolfcosplay: {Jan:11, ?, ?, ?},
    ...
}

