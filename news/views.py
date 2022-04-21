from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import get_object_or_404, render

from .models import News


def news_list(request):
    object_list = News.objects.all()
    paginator = Paginator(object_list, 5)  # По 5 на каждой странице.
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не является целым числом, возвращаем первую страницу.
        news = paginator.page(1)
    except EmptyPage:
        # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
        news = paginator.page(paginator.num_pages)
    return render(request, 'news/news/list.html', {'page': page, 'news': news})


def news_detail(request, news):
    news = get_object_or_404(News, slug=news)
    return render(request, 'news/news/detail.html', {'news': news})


def rules(request):
    return render(request, 'news/news/rules.html')
