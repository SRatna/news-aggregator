from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$',views.articles_list,name='articles_list')
]