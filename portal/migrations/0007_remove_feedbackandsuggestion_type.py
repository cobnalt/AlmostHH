# Generated by Django 4.0.3 on 2022-04-12 07:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0006_feedbackandsuggestion_vacancy_resumes_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feedbackandsuggestion',
            name='type',
        ),
    ]
