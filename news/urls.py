from django.urls import path

from . import views
from news.views import NewsList, NewsDetail, RulesView, ContactView

app_name = 'news'

urlpatterns = [
    # news views
    path(r'', NewsList.as_view()),
    # path('', views.news_list, name='news_list'),
    path(r'news/<slug:news>/', NewsDetail.as_view(), name='news_detail'),
    # path('news/<slug:news>/', views.news_detail, name='news_detail'),
    path(r'rules/', RulesView.as_view(), name='rules'),
    # path('rules/', views.rules, name='rules'),
    path(r'contact/', ContactView.as_view(), name='contact'),
    # path(r'contact/', views.contact, name='contact'),
]
