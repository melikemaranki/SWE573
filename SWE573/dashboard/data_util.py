# Import package
import json
from django.http import JsonResponse
from django_q.tasks import async_task
import tweepy
from .myCredentials import access_token, access_token_secret, consumer_key, consumer_secret, bearer
from tweepy import StreamListener, Stream, Cursor
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
import spacy
from django.shortcuts import render 

# Initialize spacy 'en' model, keeping only tagger component needed for lemmatization
nlp = spacy.load('en_core_web_sm', disable=['parser', 'ner'])

import string

sentence = "The striped bats are hanging on their feet for best"


doc = nlp(sentence)

# Extract the lemma for each token and join
" ".join([token.lemma_ for token in doc])
#> 'the strip bat be hang on -PRON- foot for good'

def getData(request, text):
    #search = Cursor(api.search, q = query, lang = 'en'). items(200)
    #s =  Search()
    #s.save()
    #s_id = Search.objects.latest("search_id").pk
    date =  timezone.now()
    user = str(request.user)

    #to get rid of timeout errors table writing task is run async
    s_id = 2
    async_task(write_table_v1, "netflix", user, s_id, date, hook=deneme)
    #async_task(deneme, "çalışıyor")
    return s_id  

def deneme(request):
    return HttpResponse('<h1>Hello HttpResponse</h1>')  

#Data collection function for Twitter API v1.1
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

            #removes search keyword
            s = s.replace(text, "")
            s = s.translate(str.maketrans('', '', string.punctuation))
            tweet.text = s
            # Parse the sentence using the loaded 'en' model object `nlp`
            lemma_nlp = nlp(tweet.text)
            # Extract the lemma for each token and join
            lemma = " ".join([token.lemma_ for token in lemma_nlp])
            
            query = Tweets(user = user, tweet_id = tweet.id, tweet_text = tweet.text, tweet_text_lemma = lemma,
            search_keyword = text, search_id = s_id, query_datetime = date)
            query.save()
        
    print("v1 async task bitti",Tweets.objects.filter(search_id = s_id).count())
    


#Data collection function for Twitter API v2
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
        list_of_splitted_tweets = [tweet.split() for tweet in df.tweet_text_lemma]
        query_words = {"could", "got", "like", "&amp;","amp", '-PRON-', '…','•','’', '"','’s','🤩','🤣'} 
        stopwords_final = query_words.union(nltk_stopwords)
        words_cleaned =  [[word for word in tweets if not word in stopwords_final and not word.isnumeric()]
                        for tweets in list_of_splitted_tweets]
        # Flatten list of words in clean tweets
        all_words = list(itertools.chain(*words_cleaned))
        t1 = time.time()
        print("stopword_cleaning",t1-t0)
        return all_words




nltk_stopwords = {'a',
 'about',
 'above',
 'after',
 'again',
 'against',
 'ain',
 'all',
 'am',
 'an',
 'and',
 'any',
 'are',
 'aren',
 "aren't",
 'as',
 'at',
 'be',
 'because',
 'been',
 'before',
 'being',
 'below',
 'between',
 'both',
 'but',
 'by',
 'can',
 'couldn',
 "couldn't",
 'd',
 'did',
 'didn',
 "didn't",
 'do',
 'does',
 'doesn',
 "doesn't",
 'doing',
 'don',
 "don't",
 'down',
 'during',
 'each',
 'few',
 'for',
 'from',
 'further',
 'had',
 'hadn',
 "hadn't",
 'has',
 'hasn',
 "hasn't",
 'have',
 'haven',
 "haven't",
 'having',
 'he',
 'her',
 'here',
 'hers',
 'herself',
 'him',
 'himself',
 'his',
 'how',
 'i',
 'if',
 'in',
 'into',
 'is',
 'isn',
 "isn't",
 'it',
 "it's",
 'its',
 'itself',
 'just',
 'll',
 'm',
 'ma',
 'me',
 'mightn',
 "mightn't",
 'more',
 'most',
 'mustn',
 "mustn't",
 'my',
 'myself',
 'needn',
 "needn't",
 'no',
 'nor',
 'not',
 'now',
 'o',
 'of',
 'off',
 'on',
 'once',
 'only',
 'or',
 'other',
 'our',
 'ours',
 'ourselves',
 'out',
 'over',
 'own',
 're',
 's',
 'same',
 'shan',
 "shan't",
 'she',
 "she's",
 'should',
 "should've",
 'shouldn',
 "shouldn't",
 'so',
 'some',
 'such',
 't',
 'than',
 'that',
 "that'll",
 'the',
 'their',
 'theirs',
 'them',
 'themselves',
 'then',
 'there',
 'these',
 'they',
 'this',
 'those',
 'through',
 'to',
 'too',
 'under',
 'until',
 'up',
 've',
 'very',
 'was',
 'wasn',
 "wasn't",
 'we',
 'were',
 'weren',
 "weren't",
 'what',
 'when',
 'where',
 'which',
 'while',
 'who',
 'whom',
 'why',
 'will',
 'with',
 'won',
 "won't",
 'wouldn',
 "wouldn't",
 'y',
 'you',
 "you'd",
 "you'll",
 "you're",
 "you've",
 'your',
 'yours',
 'yourself',
 'yourselves'}
