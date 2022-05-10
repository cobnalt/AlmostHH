# Generated by Django 4.0.3 on 2022-05-10 08:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, unique=True, verbose_name='Наименование')),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True, verbose_name='Слаг')),
                ('description', models.TextField(blank=True, max_length=700, verbose_name='Описание')),
                ('logo', models.ImageField(blank=True, upload_to='companies/<django.db.models.fields.SlugField>/', verbose_name='Лого')),
                ('contact', models.TextField(max_length=200, verbose_name='Контакты')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('send', 'Отправлено'), ('published', 'Опубликовано'), ('rework', 'На доработку')], default='draft', max_length=15, verbose_name='Статус')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Регистратор')),
            ],
        ),
        migrations.CreateModel(
            name='FeedbackAndSuggestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('send', 'Отправлено'), ('viewed', 'Просмотрено'), ('invite', 'Приглашение'), ('failure', 'Отказ')], default='send', max_length=15, verbose_name='Статус')),
            ],
        ),
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Наименование вакансии')),
                ('slug', models.SlugField(max_length=100, verbose_name='Слаг')),
                ('salary', models.CharField(max_length=150, verbose_name='Зарплата')),
                ('employment', models.CharField(max_length=150, verbose_name='Занятость')),
                ('schedule', models.CharField(max_length=150, verbose_name='График работы')),
                ('about_me', models.TextField(verbose_name='Обо мне')),
                ('education', models.TextField(verbose_name='Образование')),
                ('language', models.CharField(max_length=200, verbose_name='Знание языков')),
                ('citizenship', models.CharField(max_length=50, verbose_name='Гражданство')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('send', 'Отправлено'), ('published', 'Опубликовано'), ('rework', 'На доработку')], default='draft', max_length=15, verbose_name='Статус')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resumes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Наименование')),
                ('slug', models.SlugField(max_length=100, verbose_name='Слаг')),
                ('salary', models.CharField(max_length=150, verbose_name='Зарплата')),
                ('description', models.TextField(verbose_name='Описание вакансии')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес вакансии')),
                ('publish', models.DateTimeField(default=django.utils.timezone.now)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('send', 'Отправлено'), ('published', 'Опубликовано'), ('rework', 'На доработку')], default='draft', max_length=15, verbose_name='Статус')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vacancies', to='portal.companycard', verbose_name='Компания')),
                ('resumes', models.ManyToManyField(related_name='vacancies', through='portal.FeedbackAndSuggestion', to='portal.resume')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(blank=True, upload_to='users/', verbose_name='Фото')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('contact', models.TextField(max_length=200, verbose_name='Контакты')),
                ('living_city', models.CharField(max_length=50, verbose_name='Город проживания')),
                ('sex', models.CharField(choices=[('male', 'Мужчина'), ('female', 'Женщина')], default='male', max_length=15, verbose_name='Пол')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True, max_length=1000, verbose_name='Текст')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('feedback', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='portal.feedbackandsuggestion', verbose_name='Отклик')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_messages', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
            ],
        ),
        migrations.AddField(
            model_name='feedbackandsuggestion',
            name='resume',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', to='portal.resume', verbose_name='Резюме'),
        ),
        migrations.AddField(
            model_name='feedbackandsuggestion',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='suggestions', to='portal.vacancy', verbose_name='Вакансия'),
        ),
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateField(verbose_name='Начало работы')),
                ('finish', models.DateField(default=django.utils.timezone.now, verbose_name='Окончание работы')),
                ('untilnow', models.BooleanField(default=True, verbose_name='До настоящего времени')),
                ('organisation_name', models.CharField(max_length=100, verbose_name='Наименование организации')),
                ('position', models.CharField(max_length=100, verbose_name='Должность')),
                ('function', models.TextField(verbose_name='Обязанности')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='experiences', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'ordering': ('-finish',),
            },
        ),
    ]
