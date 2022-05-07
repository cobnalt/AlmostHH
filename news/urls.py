from django.urls import path

from . import views

app_name = 'news'

urlpatterns = [
    # news views
    path('', views.news_list, name='news_list'),
    path('news/<slug:news>/', views.news_detail, name='news_detail'),
    path('rules/', views.rules, name='rules'),
    path('contact/', views.contact, name='contact'),
]
