# Generated by Django 4.0.3 on 2022-04-05 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_alter_experience_options_remove_experience_resume_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resume',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='comment',
            field=models.TextField(blank=True, verbose_name='Комментарий'),
        ),
    ]