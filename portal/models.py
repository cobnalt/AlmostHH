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
    title = models.CharField(max_length=100, verbose_name='Наименование',
                             unique=True)
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Слаг',
                            blank=True, null=True)
    description = models.TextField(max_length=700, verbose_name='Описание',
                                   blank=True)
    logo = models.ImageField(upload_to=f'companies/{slug}/', blank=True,
                             verbose_name='Лого')
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Регистратор')
    contact = models.TextField(max_length=200, verbose_name='Контакты')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,
                              default='draft',
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
    salary = models.CharField(max_length=150, verbose_name='Зарплата')
    company = models.ForeignKey(CompanyCard, on_delete=models.CASCADE,
                                verbose_name='Компания',
                                related_name='vacancies')
    description = models.TextField(verbose_name='Описание вакансии')
    address = models.CharField(max_length=200, verbose_name='Адрес вакансии')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,
                              default='draft',
                              verbose_name='Статус')
    resumes = models.ManyToManyField('Resume', through='FeedbackAndSuggestion',
                                     through_fields=('vacancy', 'resume'),
                                     related_name='vacancies')

    def __str__(self):
        return self.title


class Resume(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Черновик'),
        ('send', 'Отправлено'),
        ('published', 'Опубликовано'),
        ('rework', 'На доработку'),
    )
    title = models.CharField(max_length=100,
                             verbose_name='Наименование вакансии')
    slug = models.SlugField(max_length=100, verbose_name='Слаг')
    salary = models.CharField(max_length=150, verbose_name='Зарплата')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='resumes')
    employment = models.CharField(max_length=150, verbose_name='Занятость')
    schedule = models.CharField(max_length=150, verbose_name='График работы')
    about_me = models.TextField(verbose_name='Обо мне')
    education = models.TextField(verbose_name='Образование')
    language = models.CharField(max_length=200, verbose_name='Знание языков')
    citizenship = models.CharField(max_length=50, verbose_name='Гражданство')
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,
                              default='draft',
                              verbose_name='Статус')

    def __str__(self):
        return self.title


class Experience(models.Model):
    start = models.DateField(verbose_name='Начало работы')
    finish = models.DateField(verbose_name='Окончание работы',
                              default=timezone.now)
    until_now = models.BooleanField(verbose_name='До настоящего времени',
                                    default=True)
    organisation_name = models.CharField(max_length=100,
                                         verbose_name='Наименование организации')
    position = models.CharField(max_length=100, verbose_name='Должность')
    function = models.TextField(verbose_name='Обязанности')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='experiences',
                             verbose_name='Пользователь', blank=True, null=True)

    class Meta:
        ordering = ('-finish',)


class Profile(models.Model):
    SEX_CHOICES = (
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    photo = models.ImageField(upload_to='users/', blank=True,
                              verbose_name='Фото')
    date_of_birth = models.DateField(blank=True, null=True,
                                     verbose_name='Дата рождения', )
    contact = models.TextField(max_length=200, verbose_name='Контакты')
    living_city = models.CharField(max_length=50,
                                   verbose_name='Город проживания')
    sex = models.CharField(max_length=15, choices=SEX_CHOICES, default='male',
                           verbose_name='Пол')

    def __str__(self):
        return f'Профиль для пользователя {self.user.username}'


class FeedbackAndSuggestion(models.Model):
    STATUS_CHOICES = (
        ('send', 'Отправлено'),
        ('viewed', 'Просмотрено'),
        ('invite', 'Приглашение'),
        ('failure', 'Отказ'),
    )
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE,
                                related_name='suggestions', verbose_name='Вакансия')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE,
                               related_name='feedbacks', verbose_name='Резюме')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES,
                              verbose_name='Статус', default='send')

    def __str__(self):
        return f'Feedback {self.id}'


class Message(models.Model):
    text = models.TextField(max_length=1000, verbose_name='Текст', blank=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='user_messages',
                               verbose_name='Отправитель',
                               blank=True, null=True)
    feedback = models.ForeignKey(FeedbackAndSuggestion,
                                 on_delete=models.CASCADE,
                                 related_name='messages',
                                 verbose_name='Отклик')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message {self.id}'
