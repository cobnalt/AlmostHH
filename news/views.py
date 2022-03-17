from django.shortcuts import render, get_object_or_404
from .models import News


def news_list(request):
    news = News.objects.all()
    return render(request, 'news/news/list.html', {'news': news})


def news_detail(request, news):
    news = get_object_or_404(News, slug=news)
    return render(request, 'news/news/detail.html', {'news': news})
