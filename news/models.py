from django.db import models
from django.urls import reverse


class News(models.Model):
    title = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг')
    body = models.TextField(verbose_name='Текст новости')
    publish = models.DateTimeField(auto_now_add=True, verbose_name='Дата опубликования')

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail', args=[self.slug])
