from django.shortcuts import render, redirect

from news.forms import FeedForm
from .models import Article,Feed
# Create your views here.

def articles_list(request):
    articles = Article.objects.all()
    return render(request,'news/articles_list.html',{'articles':articles})

def feeds_list(request):
    feeds = Feed.objects.all()
    return render(request,'news/feeds_list.html',{'feeds':feeds})

def new_feed(request):
    if request.method=='POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            feed.title='Title'
            feed.save()
            return redirect('feeds_list')
    else:
        form = FeedForm()
    return render(request,'news/new_feed.html',{'form':form})