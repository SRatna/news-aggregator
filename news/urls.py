from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$',views.articles_list, name='articles_list'),
    url(r'^feeds/new/$', views.new_feed, name='new_feed'),
    url(r'^feeds/$', views.feeds_list, name='feeds_list'),
]