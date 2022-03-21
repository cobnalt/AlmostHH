from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .forms import LoginForm, UserRegistrationForm, UserEditForm, \
    ProfileEditForm, CompanyCardEditForm
from .models import CompanyCard, Profile


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
                return render(request, 'portal/account/dashboard.html', {'section': 'dashboard'})
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
    return render(request, 'portal/account/dashboard.html', {'section': 'dashboard'})


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
    return render(request, 'portal/account/private.html', {'section': 'private',
                                                           'company_card': company_card})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
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
