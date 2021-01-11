from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from .data_util import getData
from .image_util import get_plot, get_wordcloud

@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')


def showResults(request):
    if request.method == 'GET':
        # Create a form instance and populate it with data from the request (binding):
        text = request.GET['search']
        data = getData(text)
        chart =  get_plot(data)
        #wcloud = get_wordcloud(data)
        return render(request, 'dashboard/showResults.html', {"search": text, "chart":chart})#, "wcloud":wcloud"""})
