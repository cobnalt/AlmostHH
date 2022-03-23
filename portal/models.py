from django.contrib.auth.models import User
from django.utils import timezone
from django.db import models


class CompanyCard(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('send', 'Отправлено'),
        ('published', 'Опубликовано'),
        ('rework', 'На доработку'),
    )
    title = models.CharField(max_length=100, verbose_name='Наименование', unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг', blank=True, null=True)
    description = models.TextField(max_length=700, verbose_name='Описание', blank=True)
    logo = models.ImageField(upload_to=f'companies/{slug}/', blank=True, verbose_name='Лого')
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Регистратор')
    contact = models.TextField(max_length=200, verbose_name='Контакты')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft',
                              verbose_name='Статус')

    def __str__(self):
        return self.title


class Vacancy(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('send', 'Отправлено'),
        ('published', 'Опубликовано'),
        ('rework', 'На доработку'),
    )
    title = models.CharField(max_length=100, verbose_name='Наименование')
    slug = models.SlugField(max_length=100, verbose_name='Слаг')
    salary = models.TextField(max_length=150, verbose_name='Зарплата')
    company = models.ForeignKey(CompanyCard, on_delete=models.CASCADE,
                                verbose_name='Компания', related_name='vacancies')
    description = models.TextField(verbose_name='Описание вакансии')
    address = models.CharField(max_length=200, verbose_name='Адрес вакансии')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft',
                              verbose_name='Статус')

    def __str__(self):
        return self.title


class Profile(models.Model):
    SEX_CHOICES = (
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    photo = models.ImageField(upload_to='users/', blank=True,
                              verbose_name='Фото')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения',)
    contact = models.TextField(max_length=200, verbose_name='Контакты')
    living_city = models.CharField(max_length=50, verbose_name='Город проживания')
    sex = models.CharField(max_length=15, choices=SEX_CHOICES, default='male',
                           verbose_name='Пол')

    def __str__(self):
        return f'Профиль для пользователя {self.user.username}'
