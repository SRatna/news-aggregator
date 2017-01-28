from django.shortcuts import render, redirect

from news.forms import FeedForm
from .models import Article,Feed
import datetime
import feedparser
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
            feedData = feedparser.parse(feed.url)
            feed.title = feedData.feed.title
            feed.save()
            for entry in feedData.entries:
                try:
                    article = Article()
                    article.title = entry.title
                    article.feed = feed
                    article.description = entry.description
                    article.url = entry.link

                    d = datetime.datetime(*(entry.published_parsed[0:6]))
                    dateString = d.strftime('%Y-%m-%d %H:%M:%S')
                    article.published_date = dateString

                    article.save()
                except:
                    pass
            return redirect('feeds_list')
    else:
        form = FeedForm()
    return render(request,'news/new_feed.html',{'form':form})