from django.shortcuts import render, redirect

from news.forms import FeedForm
from .models import Article,Feed
import datetime
import feedparser
# Create your views here.

def articles_list(request):
    articles = Article.objects.all()
    rows = [articles[x:x+2] for x in range(0,len(articles),2)]
    return render(request,'news/articles_list.html',{'rows':rows})

def articles_list_of_a_feed(request,a_feed):
    articles = Article.objects.filter(feed__title=a_feed)
    rows = [articles[x:x+2] for x in range(0,len(articles),2)]
    return render(request,'news/articles_list.html',{'rows':rows})

def feeds_list(request):
    feeds = Feed.objects.all()
    return render(request,'news/feeds_list.html',{'feeds':feeds})

def new_feed(request):
    if request.method=='POST':
        form = FeedForm(request.POST)
        if form.is_valid():
            feed = form.save(commit=False)
            #check whether the url is already existing or not
            existingFeed = Feed.objects.filter(url=feed.url)
            if(len(existingFeed)==0):
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