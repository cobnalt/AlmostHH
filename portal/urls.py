from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.register, name='register'),
    path('', views.dashboard, name='dashboard'),
    path('private/', views.private, name='private'),
    path('edit_company_card/', views.edit_company_card, name='edit_company_card'),
    ]
