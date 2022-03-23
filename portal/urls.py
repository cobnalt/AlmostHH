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
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('my_vacancies/', views.my_vacancies, name='my_vacancies'),
    path('add_vacancy/', views.add_vacancy, name='add_vacancy'),
    path('edit_vacancy/<int:vacancy_id>/', views.edit_vacancy, name='edit_vacancy'),
    path('delete_vacancy/<int:vacancy_id>/', views.delete_vacancy, name='delete_vacancy'),
    ]
