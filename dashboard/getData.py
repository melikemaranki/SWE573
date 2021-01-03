# Import package
import json
import tweepy
from .myCredentials import access_token, access_token_secret, consumer_key, consumer_secret
from tweepy import StreamListener
from tweepy import Stream
from tweepy import Cursor
import pandas as pd
from pandas import DataFrame
from nltk import bigrams
import nltk
import itertools
from nltk.corpus import stopwords

def getData(text):
    # Pass OAuth details to tweepy's OAuth handler
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    ##public_tweets = api.home_timeline()
    query = text +" -filter:retweets"
    search = Cursor(api.search, q = query, lang = 'en'). items(100)


    list_of_dicts = []
    for tweet in search:
        list_of_dicts.append({'tweet' :tweet.text, 'created_at':tweet.created_at})

    df= DataFrame.from_dict(list_of_dicts)


    # Download stopwords
    nltk.download('stopwords')
    stop_words = set(stopwords.words('english'))
    #textblob
    list_of_splitted_tweets = [tweet.replace("!","").lower().split() for tweet in df.tweet]

    query_words = ["covid-19", "covid",'''separate query stop words from others''' "could", "got", "like", "&amp;", "-", "|"]
    stop_words.update(query_words)
    stop_words
    words_cleaned =  [[word for word in tweets if not word in stop_words]
                    for tweets in list_of_splitted_tweets]


    # Flatten list of words in clean tweets
    all_words = list(itertools.chain(*words_cleaned))
    return all_words    
   