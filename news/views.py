from .models import News
from django.views.generic import TemplateView, ListView, DetailView


class NewsList(ListView):
    model = News
    template_name = 'news/news/list.html'
    context_object_name = 'news'
    paginate_by = 3


class IndexView(TemplateView):
    template_name = 'news/index.html'


class ContactView(TemplateView):
    template_name = 'news/contact.html'


class NewsDetail(DetailView):
    model = News
    slug_url_kwarg = 'news'
    template_name = 'news/news/detail.html'
    context_object_name = 'news'


class RulesView(TemplateView):
    template_name = 'news/news/rules.html'
