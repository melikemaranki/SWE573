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
    tweet_text_lemma = models.CharField(default = "", max_length=500)
    search_id = models.IntegerField(default = 0)

class Search(models.Model):
    search_id = models.AutoField(primary_key=True)

