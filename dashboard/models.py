from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Tweets(models.Model):
    query_datetime = models.DateTimeField(default = timezone.now)
    search_keyword = tweet_text = models.CharField(default = "", max_length=100)
    tweet_id = models.IntegerField()
    tweet_text = models.CharField(max_length=280)