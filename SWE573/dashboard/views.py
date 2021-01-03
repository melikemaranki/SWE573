from django.shortcuts import render 
from django.contrib.auth.decorators import login_required
from .getData import getData
from .utils import get_plot

@login_required
def profile(request):
    return render(request, 'dashboard/profile.html')


def showResults(request):
    if request.method == 'GET':
        # Create a form instance and populate it with data from the request (binding):
        text = request.GET['search']
        data = getData(text)
        chart =  get_plot(data)
        return render(request, 'dashboard/showResults.html', {"search": text, "chart":chart})