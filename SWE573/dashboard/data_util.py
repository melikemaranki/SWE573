# Import package
import json
from django.http import JsonResponse
from django_q.tasks import async_task
import tweepy
from .myCredentials import access_token, access_token_secret, consumer_key, consumer_secret, bearer
from tweepy import StreamListener
from tweepy import Stream
from tweepy import Cursor
import pandas as pd
from pandas import DataFrame
#from nltk import bigrams
import nltk
import itertools
from nltk.corpus import stopwords
import re
from django.utils import timezone
from dashboard.models import Tweets, Search
import time
import requests
from django_q.tasks import async_task, result
# Use the schedule wrapper
from django_q.tasks import schedule, Schedule
from django.http import HttpResponse


import string


def getData(request, text):
    #search = Cursor(api.search, q = query, lang = 'en'). items(200)
    s =  Search()
    s.save()
    s_id = Search.objects.latest("search_id").pk
    date =  timezone.now()
    user = str(request.user)
    #to get rid of timeout errors table writing task is run async
    async_task(write_table_v1, text, user, s_id, date)#, hook=showChart)
    async_task(deneme, "çalışıyor")
    return s_id  

def deneme(s):
    print(s)


def write_table_v1(text, user, s_id, date):
   # Pass OAuth details to tweepy's OAuth handler
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    #api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    ##public_tweets = api.home_timeline()
    query = text +" -filter:retweets"
    
    search = Cursor(api.search, q = query, lang = 'en'). items(1000)
    print(search)
    try:
        search.next()
    except StopIteration:
        # Code here for the case where the iterator is empty
        return ""
    else:

        for tweet in search:
            s = remove_emoji(re.sub(r'http\S+', '', tweet.text)).lower()
            s = s.replace(text, "")
            tweet.text = s.translate(str.maketrans('', '', string.punctuation))
            query = Tweets(user = user, tweet_id = tweet.id, tweet_text = tweet.text, search_keyword = text, search_id = s_id, query_datetime = date)
            query.save()
        
    print("v1 async task bitti",Tweets.objects.filter(search_id = s_id).count())
        


def write_table_v2(text, user, s_id, date):
    url = 'https://api.twitter.com/2/tweets/search/recent'
    headers = {
    'content-type': 'application/json',
    "Authorization": bearer
    }
    query = text +' -is:retweet lang:en'
    max_result = 10
    params = {
    'max_results': max_result,
    'query': query,
    'tweet.fields': 'created_at,public_metrics,context_annotations,entities'
    }  
    repeat = 1
    for i in range(repeat):
        response = requests.get(url, params=params, headers=headers).json()
        #prep_data_with_response(response)
        if(response['meta']['next_token'] is not None):
            params['next_token'] = response['meta']['next_token']
        df= DataFrame.from_dict(response['data'])[['text', 'id']]

        print("uzunluk",len(df.index))
        #user_mention = []
        for index in df.index: 
            s = remove_emoji(re.sub(r'http\S+', '', df['text'][index])).lower()
            s = s.replace(text, "")
            df['text'][index] = s.translate(str.maketrans('', '', string.punctuation))
            query = Tweets(user = user, tweet_id = df['id'][index], tweet_text = df['text'][index], search_keyword = text, search_id = s_id, query_datetime = date)
            query.save()    
        print(Tweets.objects.filter(search_id = s_id).count())

# Reference : https://gist.github.com/slowkow/7a7f61f495e3dbb7e3d767f97bd7304b
def remove_emoji(string):
    emoji_pattern = re.compile("["
                           u"\U0001F600-\U0001F64F"  # emoticons
                           u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                           u"\U0001F680-\U0001F6FF"  # transport & map symbols
                           u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           u"\U00002702-\U000027B0"
                           u"\U000024C2-\U0001F251"
                           "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', string) 

def clean_stopwords(df):
        t0 = time.time()    
        # Download stopwords
        #nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        #textblob
        list_of_splitted_tweets = [tweet.split() for tweet in df.tweet_text]
        query_words = ["covid-19", "covid", "could", "got", "like", "&amp;", "-", "|","\"","'"]
        stop_words.update(query_words)
        words_cleaned =  [[word for word in tweets if not word in stop_words]
                        for tweets in list_of_splitted_tweets]
        # Flatten list of words in clean tweets
        all_words = list(itertools.chain(*words_cleaned))
        t1 = time.time()
        print("stopword_cleaning",t1-t0)
        return all_words
