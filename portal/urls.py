from django.urls import path

from . import views

app_name = 'portal'

urlpatterns = [
    # path('login/', views.user_login, name='login'),
    path(r'login/', views.UserLogin.as_view(), name='login'),
    # path('logout/', views.user_logout, name='logout'),
    path(r'logout/', views.UserLogout.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # path('', views.dashboard, name='dashboard'),
    path(r'', views.Dashboard.as_view(), name='dashboard'),
    # path('private/', views.private, name='private'),
    path(r'private/', views.Private.as_view(), name='private'),

    path('edit_company_card/', views.edit_company_card, name='edit_company_card'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

    # path('my_vacancies/', views.my_vacancies, name='my_vacancies'),
    path(r'my_vacancies/', views.MyVacancies.as_view(), name='my_vacancies'),
    path('vacancy/<int:vacancy_id>/', views.vacancy_detail, name='vacancy_detail'),
    path('add_vacancy/', views.add_vacancy, name='add_vacancy'),
    path('edit_vacancy/<int:vacancy_id>/', views.edit_vacancy, name='edit_vacancy'),
    # path('delete_vacancy/<int:vacancy_id>/', views.delete_vacancy, name='delete_vacancy'),
    path('delete_vacancy/<int:vacancy_id>/', views.DeleteVacancy.as_view(), name='delete_vacancy'),

    # path('my_resumes/', views.my_resumes, name='my_resumes'),
    path(r'my_resumes/', views.MyResumes.as_view(), name='my_resumes'),
    path('resume/<int:resume_id>/', views.resume_detail, name='resume_detail'),
    path('add_resume/', views.add_resume, name='add_resume'),
    path('edit_resume/<int:resume_id>/', views.edit_resume, name='edit_resume'),
    # path('delete_resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('delete_resume/<int:resume_id>/', views.DeleteResume.as_view(), name='delete_resume'),


    path('add_experience/', views.add_experience, name='add_experience'),
    path('edit_experience/<int:exp_id>/', views.edit_experience,
         name='edit_experience'),
    path('delete_experience/<int:exp_id>/', views.delete_experience,
         name='delete_experience'),

    # path('find_resume/', views.find_resume, name='find_resume'),
    path('find_resume/', views.FindResume.as_view(), name='find_resume'),
    # path('find_job/', views.find_job, name='find_job'),
    path('find_job/', views.FindJob.as_view(), name='find_job'),

    path('feedback-and-suggestion/', views.feedback_list, name='feedback_list'),
    path('feedback-and-suggestion/<int:feedback_id>/', views.feedback_detail, name='feedback_detail'),
    ]
