from django.contrib import admin
from django.db import models
from tinymce.widgets import TinyMCE
from .models import News


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('publish',)
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
