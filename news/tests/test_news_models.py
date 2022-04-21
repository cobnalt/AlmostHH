from datetime import datetime, timedelta

from django.test import TestCase

from news.models import News


class NewsModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        News.objects.create(
            title='Some Title',
            slug='some-title',
            body='Some news body text',
            publish=datetime.now() - timedelta(2),
        )

    def test_title_label(self):
        news = News.objects.get(id=1)
        field_label = news._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Наименование')

    def test_title_max_length(self):
        news = News.objects.get(id=1)
        field_nax_length = news._meta.get_field('title').max_length
        self.assertEquals(field_nax_length, 100)

    def test_slug_label(self):
        news = News.objects.get(id=1)
        field_label = news._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Слаг')

    def test_slug_max_length(self):
        news = News.objects.get(id=1)
        field_nax_length = news._meta.get_field('slug').max_length
        self.assertEquals(field_nax_length, 100)

    def test_body_label(self):
        news = News.objects.get(id=1)
        field_label = news._meta.get_field('body').verbose_name
        self.assertEquals(field_label, 'Текст новости')

    def test_publish_label(self):
        news = News.objects.get(id=1)
        field_label = news._meta.get_field('publish').verbose_name
        self.assertEquals(field_label, 'Дата опубликования')

    def test_object_repr(self):
        news = News.objects.get(id=1)
        expected_object_name = news.title
        self.assertEquals(expected_object_name, str(news))

    def test_get_absolute_url(self):
        news = News.objects.get(id=1)

        self.assertEquals(news.get_absolute_url(), '/news/some-title/')
