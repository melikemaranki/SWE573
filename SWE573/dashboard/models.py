from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Tweets(models.Model):
    query_datetime = models.DateTimeField(default = timezone.now)
    user =  models.CharField(max_length = 256, default ="")
    search_keyword = tweet_text = models.CharField(default = "", max_length=100)
    tweet_id = models.CharField(max_length=30)
    tweet_text = models.CharField(max_length=500)
    search_id = models.IntegerField(default = 0)
    isSaved = models.BooleanField(default = False)
    #name given to the saved search by the user
    #!! 256 karakterden uzun girilirse uyarı vermesi lazım. Unutma!
    saved_search_alias = models.CharField(max_length = 256, default ="")

class Search(models.Model):
    search_id = models.AutoField(primary_key=True)
