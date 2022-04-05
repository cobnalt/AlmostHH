from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.text import slugify
from .forms import LoginForm, UserRegistrationForm, UserEditForm, \
    ProfileEditForm, CompanyCardEditForm, VacancyAddForm, ResumeAddForm,\
    ExperienceAddForm
from .models import CompanyCard, Profile, Vacancy, Resume, Experience
from django.db.models import Q


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                vacancies = Vacancy.objects.all().filter(status='published')
                resumes = Resume.objects.all().filter(status='published')
                return render(request, 'portal/account/dashboard.html',
                              {'section': 'dashboard', 'vacancies': vacancies,
                               'resumes': resumes})
            else:
                return HttpResponse("Disable Acc")
        else:
            return HttpResponse("Invalid login")
    else:
        form = LoginForm()
    return render(request, 'portal/account/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, 'portal/account/logout.html')


@login_required()
def dashboard(request):
    vacancies = Vacancy.objects.all().filter(status='published')
    resumes = Resume.objects.all().filter(status='published')
    return render(request, 'portal/account/dashboard.html',
                  {'section': 'dashboard', 'vacancies': vacancies,
                   'resumes': resumes})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Создаем нового пользователя, но пока не сохраняем в базу данных.
            new_user = user_form.save(commit=False)
            # Задаем пользователю зашифрованный пароль.
            new_user.set_password(user_form.cleaned_data['password'])
            # Сохраняем пользователя в базе данных.
            new_user.save()
            # В зависимости от роли задаем пользователю группу
            if user_form.cleaned_data['role'] == 'W':
                new_user.groups.add(Group.objects.get(name='Workers'))
                Profile.objects.create(user=new_user)
            else:
                new_user.groups.add(Group.objects.get(name='Employers'))
                CompanyCard.objects.create(user=new_user)
            return render(request, 'portal/account/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        return render(request, 'portal/account/register.html',
                      {'user_form': user_form})


@login_required()
def private(request):
    try:
        company_card = get_object_or_404(CompanyCard, user=request.user)
    except Exception:
        company_card = None
    try:
        profile = get_object_or_404(Profile, user=request.user)
    except Exception:
        profile = None
    return render(request, 'portal/account/private.html', {'section': 'private',
                                                           'company_card': company_card,
                                                           'profile': profile})


@login_required
@permission_required('portal.change_profile')
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль изменен успешно.')
        else:
            messages.error(request, 'Ошибка при изменении профиля.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'portal/account/edit_profile.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
@permission_required('portal.change_companycard')
def edit_company_card(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        company_card_form = CompanyCardEditForm(instance=request.user.companycard,
                                                data=request.POST,
                                                files=request.FILES)
        if user_form.is_valid() and company_card_form.is_valid():
            user_form.save()
            company_card_form.save()
            messages.success(request, 'Карточка компании изменена успешно.')
        else:
            messages.error(request, 'Ошибка при изменении карточки компании.')
    else:
        user_form = UserEditForm(instance=request.user)
        company_card_form = CompanyCardEditForm(instance=request.user.companycard)
    return render(request, 'portal/account/edit_company_card.html',
                  {'user_form': user_form, 'company_card_form': company_card_form})


@login_required
@permission_required('portal.add_vacancy')
def my_vacancies(request):
    vacs = Vacancy.objects.filter(company=request.user.companycard)
    return render(request, 'portal/account/my_vacancies.html', {'vacs': vacs})


@login_required
def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    return render(request, 'portal/account/vacancy_detail.html',
                  {'vacancy': vacancy})


@login_required
@permission_required('portal.add_vacancy')
def add_vacancy(request):
    if request.method == 'POST':
        vacancy_form = VacancyAddForm(request.POST)
        if vacancy_form.is_valid():
            new_vacancy = vacancy_form.save(commit=False)
            new_vacancy.company = request.user.companycard
            new_vacancy.slug = slugify(new_vacancy.title)
            new_vacancy.status = 'send' if 'moderate' in request.POST else 'draft'
            new_vacancy.save()
            messages.success(request, 'Вакансия создана успешно.')
            return redirect('portal:my_vacancies')
        else:
            messages.error(request, 'Ошибка при создании вакансии.')
    else:
        if request.user.companycard.title == "":
            messages.warning(request, 'Сначала заполните карточку компании.')
            return redirect('portal:edit_company_card')
        vacancy_form = VacancyAddForm()
    return render(request, 'portal/account/add_vacancy.html',
                  {'vacancy_form': vacancy_form})


@login_required
@permission_required('portal.change_vacancy')
def edit_vacancy(request, vacancy_id):
    edit_vac = get_object_or_404(Vacancy, pk=vacancy_id, company__user=request.user)
    comment = edit_vac.comment
    if request.method == 'POST':
        vacancy_form = VacancyAddForm(instance=edit_vac, data=request.POST)
        if vacancy_form.is_valid():
            new_vacancy = vacancy_form.save(commit=False)
            new_vacancy.company = request.user.companycard
            new_vacancy.slug = slugify(new_vacancy.title)
            new_vacancy.status = 'send' if 'moderate' in request.POST else 'draft'
            new_vacancy.save()
            messages.success(request, 'Вакансия изменена успешно.')
            return redirect('portal:my_vacancies')
        else:
            messages.error(request, 'Ошибка при создании вакансии.')
    else:
        vacancy_form = VacancyAddForm(instance=edit_vac)
    return render(request, 'portal/account/edit_vacancy.html',
                  {'vacancy_form': vacancy_form, 'comment': comment})


@login_required
@permission_required('portal.delete_vacancy')
def delete_vacancy(request, vacancy_id):
    del_vac = get_object_or_404(Vacancy, pk=vacancy_id, company__user=request.user)
    if request.method == 'POST':
        del_vac.delete()
        messages.success(request, 'Вакансия удалена успешно.')
        return redirect('portal:my_vacancies')
    else:
        context = {'del_vac': del_vac}
    return render(request, 'portal/account/delete_vacancy.html', context)


@login_required
@permission_required('portal.add_resume')
def my_resumes(request):
    resumes = Resume.objects.filter(user=request.user)
    return render(request, 'portal/account/my_resumes.html', {'resumes': resumes})


@login_required
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    return render(request, 'portal/account/resume_detail.html',
                  {'resume': resume})


@login_required
@permission_required('portal.add_resume')
def add_resume(request):
    try:
        exps = request.user.experiences.all()
    except Exception:
        exps = None
    if request.method == 'POST':
        resume_form = ResumeAddForm(request.POST)
        if resume_form.is_valid():
            new_resume = resume_form.save(commit=False)
            new_resume.slug = slugify(new_resume.title)
            new_resume.user = request.user
            new_resume.status = 'send' if 'moderate' in request.POST else 'draft'
            new_resume.save()
            messages.success(request, 'Новое резюме добавлено успешно')
            return redirect('portal:my_resumes')
        else:
            messages.error(request, 'Ошибка при добавлении резюме')
    else:
        resume_form = ResumeAddForm()
    return render(request, 'portal/account/add_resume.html',
                  {'resume_form': resume_form,
                   'experiences': exps})


@login_required
@permission_required('portal.change_resume')
def edit_resume(request, resume_id):
    edit_res = get_object_or_404(Resume, pk=resume_id, user=request.user)
    comment = edit_res.comment
    try:
        exps = request.user.experiences.all()
    except Exception:
        exps = None
    if request.method == 'POST':
        resume_form = ResumeAddForm(instance=edit_res, data=request.POST)
        if resume_form.is_valid():
            new_resume = resume_form.save(commit=False)
            new_resume.slug = slugify(new_resume.title)
            new_resume.user = request.user
            new_resume.status = 'send' if 'moderate' in request.POST else 'draft'
            new_resume.save()
            messages.success(request, 'Резюме отредактировано успешно')
            return redirect('portal:my_resumes')
        else:
            messages.error(request, 'Ошибка при редактировании резюме')
    else:
        resume_form = ResumeAddForm(instance=edit_res)
    return render(request, 'portal/account/edit_resume.html',
                  {'resume_form': resume_form, 'exps': exps, 'comment': comment})


@login_required
@permission_required('portal.delete_resume')
def delete_resume(request, resume_id):
    del_resume = get_object_or_404(Resume, pk=resume_id)
    if request.method == 'POST':
        del_resume.delete()
        messages.success(request, 'Резюме удалено успешно.')
        return redirect('portal:my_resumes')
    else:
        context = {'del_resume': del_resume}
    return render(request, 'portal/account/delete_resume.html', context)


@login_required
@permission_required('portal.add_resume')
def add_experience(request):
    if request.method == 'POST':
        exp_form = ExperienceAddForm(request.POST)
        if exp_form.is_valid():
            new_exp = exp_form.save(commit=False)
            new_exp.user = request.user
            new_exp.save()
            messages.success(request, 'Новый опыт работы добавлен успешно')
            return redirect('portal:add_resume')
        else:
            messages.error(request, 'Ошибка при добавлении опыта работы')
    else:
        exp_form = ExperienceAddForm()
    return render(request, 'portal/account/add_experience.html',
                  {'exp_form': exp_form})


@login_required
@permission_required('portal.change_resume')
def edit_experience(request, experience_id):
    pass


@login_required
@permission_required('portal.delete_resume')
def delete_experience(request, experience_id):
    pass


@login_required()
def find_resume(request):
    query = request.GET.get('q')
    resume = Resume.objects.all().filter(status='published')
    if not query:
        return render(request, 'portal/account/find_resume.html', {'resume': resume})
    resume = resume.filter(title__icontains=query)
    return render(request, 'portal/account/find_resume.html', {'resume': resume})


@login_required()
def find_job(request):
    query = request.GET.get('q')
    job = Vacancy.objects.all().filter(status='published')
    if not query:
        return render(request, 'portal/account/find_job.html', {'job': job})
    job = job.filter(title__icontains=query)
    return render(request, 'portal/account/find_job.html', {'job': job})
