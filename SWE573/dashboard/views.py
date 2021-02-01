from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .data_util import getData
from .image_util import get_plot, get_wordcloud, get_network
import itertools, collections
from dashboard.models import Tweets, Search
from pandas import DataFrame
from .data_util import clean_stopwords
import time



@login_required
def profile(request):
    q_res = MyView(request)
    return render(request, 'dashboard/profile.html', {'q_res': q_res})

def MyView(request):
    #Getting the last 5 searches of the requesting user
    query_results = Tweets.objects.filter(user=request.user).distinct("search_id").order_by("-search_id")[:5]
    return query_results
    #return a response to your template and add query_results to the context

def fetchData(request):
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        text = request.POST['search']
        if not text.strip():
            return
        s_id = getData(request = request, text = text)
        q_res = MyView(request)
        #s_id = Tweets.objects.filter(user=request.user).latest("search_id").search_id
    return render(request, 'dashboard/profile.html', {"search": text,  "search_id":s_id, "q_res":q_res})


def showChart_with_ID(request):
    if request.method == 'POST':
        s_id = request.POST['id']
    else:
        s_id = 1 #renders precollected covid database.
    
    tweet_count = Tweets.objects.filter(search_id=s_id).count()
    df = DataFrame.from_dict(Tweets.objects.filter(search_id = s_id).values("tweet_text_lemma"))
    kword = Tweets.objects.filter(search_id = s_id).values("search_keyword")[0]
    data =  clean_stopwords(df)
    chart = get_plot(data)
    wcloud = get_wordcloud(data)
    network = get_network(data)
    q_res = MyView(request)
    return render(request, 'dashboard/profile.html', {"chart": chart, "wcloud":wcloud, "network":network,
    "s_test":s_id, "count": tweet_count, 'q_res': q_res, "kword": kword})