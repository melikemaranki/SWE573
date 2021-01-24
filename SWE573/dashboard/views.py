from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from .data_util import getData
from .image_util import get_plot, get_wordcloud
import itertools, collections
from dashboard.models import Tweets, Search
from pandas import DataFrame
from .data_util import clean_stopwords
import time

@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')


def fetchData(request):
    if request.method == 'GET':
        # Create a form instance and populate it with data from the request (binding):
        text = request.GET['search']
        s_id = getData(request = request, text = text)
        
        #s_id = Tweets.objects.filter(user=request.user).latest("search_id").search_id
        return render(request, 'dashboard/showResults.html', {"search": text,  "search_id":s_id})

def showChart(request):
    s_id = Tweets.objects.filter(user=request.user).latest("search_id").search_id
    tweet_count = Tweets.objects.filter(search_id=s_id).count()
    df = DataFrame.from_dict(Tweets.objects.filter(search_id = s_id).values("tweet_text"))
    data =  clean_stopwords(df)
    chart = get_plot(data)
    wcloud = get_wordcloud(data)
    return render(request, 'dashboard/showResults.html', {"chart": chart, "wcloud":wcloud,  "s_test":s_id, "count": tweet_count})