# Import package
import json
import tweepy
from .myCredentials import access_token, access_token_secret, consumer_key, consumer_secret
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
from dashboard.models import Tweets

def getData(text):
    # Pass OAuth details to tweepy's OAuth handler
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    #api = tweepy.API(auth)
    api = tweepy.API(auth, wait_on_rate_limit=True)
    ##public_tweets = api.home_timeline()
    query = text +" -filter:retweets"
    search = Cursor(api.search, q = query, lang = 'en'). items(10)

    try:
        search.next()
    except StopIteration:
        # Code here for the case where the iterator is empty
        return ""
    else:
        list_of_dicts = []
        #user_mention = []
        for tweet in search:
            tweet.text = remove_emoji(re.sub(r'http\S+', '', tweet.text))

            """is_sensitive = tweet.possibly_sensitive if hasattr(tweet, 'possibly_sensitive') else ""
            url = "" if DataFrame.from_dict(tweet.entities['urls']).empty else DataFrame.from_dict(tweet.entities['urls']).url[0]"""
            """list_of_dicts.append({'tweet_id':tweet.id,  
                                'tweet' :tweet.text, 
                                'created_at':tweet.created_at,
                                'url' : url, 
                                'friends_count': tweet.user.friends_count, 
                                'followers_count':tweet.user.followers_count, 
                                "is_sensitive": is_sensitive})"""
            list_of_dicts.append({'tweet_id':tweet.id,  
                                'tweet' :tweet.text})
            query = Tweets(tweet_id = tweet.id, tweet_text = tweet.text, search_keyword = text)
            query.save()

        """for mention in tweet.entities['user_mentions']:
            user_mention.append({'tweet_id': tweet.id,'mentioned_user_name':mention['screen_name'],
            'mentioned_name':mention['name']})
         """
        
        
        df= DataFrame.from_dict(Tweets.objects.all().values("tweet_text"))
        # Download stopwords
        #nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        #textblob
        list_of_splitted_tweets = [tweet.lower().split() for tweet in df.tweet_text]
        query_words = ["covid-19", "covid",'''separate query stop words from others''' "could", "got", "like", "&amp;", "-", "|"]
        stop_words.update(query_words)
        words_cleaned =  [[word for word in tweets if not word in stop_words]
                        for tweets in list_of_splitted_tweets]
        # Flatten list of words in clean tweets
        all_words = list(itertools.chain(*words_cleaned))
        return all_words
  
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