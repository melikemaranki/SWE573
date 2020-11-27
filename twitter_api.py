# Import package
import json
import tweepy
import myCredentials as my

# Pass OAuth details to tweepy's OAuth handler
auth = tweepy.OAuthHandler(my.consumer_key, my.consumer_secret)
auth.set_access_token(my.access_token, my.access_token_secret)

api = tweepy.API(auth)

##public_tweets = api.home_timeline()
search = api.search(["covid","obama"], lang = 'en')
for tweet in search:
 print(tweet)

