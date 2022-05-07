# from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
# from django.shortcuts import get_object_or_404, render

from .models import News

# from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView, DetailView


class NewsList(ListView):
    model = News
    template_name = 'news/news/list.html'
    context_object_name = 'news'
    paginate_by = 3


# def news_list(request):
#     object_list = News.objects.all()
#     paginator = Paginator(object_list, 5)  # По 5 на каждой странице.
#     page = request.GET.get('page')
#     try:
#         news = paginator.page(page)
#     except PageNotAnInteger:
#         # Если страница не является целым числом, возвращаем первую страницу.
#         news = paginator.page(1)
#     except EmptyPage:
#         # Если номер страницы больше, чем общее количество страниц, возвращаем последнюю.
#         news = paginator.page(paginator.num_pages)
#     return render(request, 'news/news/list.html', {'page': page, 'news': news})


def index(request):
    return render(request, 'news/index.html')


def contact(request):
    return render(request, 'news/contact.html')


class NewsDetail(DetailView):
    model = News
    slug_url_kwarg = 'news'
    template_name = 'news/news/detail.html'
    context_object_name = 'news'


# def news_detail(request, news):
#     news = get_object_or_404(News, slug=news)
#     return render(request, 'news/news/detail.html', {'news': news})


class RulesView(TemplateView):
     template_name = 'news/news/rules.html'


# def rules(request):
#     return render(request, 'news/news/rules.html')
