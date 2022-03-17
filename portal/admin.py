from django.contrib import admin
from .models import CompanyCard, Vacancy, Profile


@admin.register(CompanyCard)
class CompanyCardAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'user')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'company', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'company')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'contact', 'living_city', 'sex')
    list_filter = ('user', 'living_city')
    search_fields = ('user', 'living_city')
    ordering = ('living_city',)
