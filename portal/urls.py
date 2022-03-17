from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    ]
