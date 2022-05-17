from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group
from django.db.models import F, Value
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from .forms import (CompanyCardEditForm, ExperienceAddForm, ExperienceFormSet,
                    MessageForm, ProfileEditForm, ResumeAddForm,
                    UserEditForm, UserRegistrationForm, VacancyAddForm)
from .models import (CompanyCard, FeedbackAndSuggestion, Message,
                     Profile, Resume, Vacancy)

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView, DeleteView
from django.urls import reverse_lazy

from common.utils.fulltextsearch import SearchResultsList


class UserLogin(LoginView):
    template_name = 'portal/account/login.html'
    success_url = 'portal/account/dashboard.html'
    extra_context = {'section': 'dashboard',
                     'vacancies': Vacancy.published.all(),
                     'resumes': Resume.published.all(),
                     }


class UserLogout(LogoutView):
    template_name = 'portal/account/logout.html'


class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'portal/account/dashboard.html'
    extra_context = {'section': 'dashboard',
                     'vacancies': Vacancy.published.all(),
                     'resumes': Resume.published.all()
                     }


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


class Private(LoginRequiredMixin, TemplateView):
    template_name = 'portal/account/private.html'

    def get_context_data(self, **kwargs):
        context = super(Private, self).get_context_data(**kwargs)

        context.update({'section': 'private',
                        'company_card': CompanyCard.objects.filter(
                            user=self.request.user).first(),
                        'profile': Profile.objects.filter(
                            user=self.request.user).first(),
                        })
        return context


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
        company_card_form = CompanyCardEditForm(
            instance=request.user.companycard,
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
        company_card_form = CompanyCardEditForm(
            instance=request.user.companycard)
    return render(request, 'portal/account/edit_company_card.html',
                  {'user_form': user_form,
                   'company_card_form': company_card_form})


class MyVacancies(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'portal/account/my_vacancies.html'
    permission_required = 'portal.add_vacancy'

    def get_context_data(self, **kwargs):
        context = super(MyVacancies, self).get_context_data(**kwargs)
        context.update({'vacs': Vacancy.objects.filter(
            company=self.request.user.companycard),
            'left_menu': 'my_vacs'}
        )
        return context


@login_required
def vacancy_detail(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    resumes = Resume.published.filter(user=request.user)
    vac_feed = FeedbackAndSuggestion.objects.filter(vacancy=vacancy)
    resumes = resumes.exclude(feedbacks__in=vac_feed)
    if request.method == 'POST':
        resume = get_object_or_404(Resume,
                                   pk=request.POST.get('active_resume'))
        FeedbackAndSuggestion.objects.create(vacancy=vacancy, resume=resume)
        messages.success(request, 'Отклик отправлен успешно.')
        return redirect('portal:vacancy_detail', vacancy_id=vacancy_id)
    return render(request, 'portal/account/vacancy_detail.html',
                  {'vacancy': vacancy, 'resumes': resumes})


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
    edit_vac = get_object_or_404(Vacancy, pk=vacancy_id,
                                 company__user=request.user)
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


class DeleteVacancy(LoginRequiredMixin, PermissionRequiredMixin,
                    SuccessMessageMixin, DeleteView):
    template_name = 'portal/account/delete_vacancy.html'
    permission_required = 'portal.delete_vacancy'
    model = Vacancy
    pk_url_kwarg = 'vacancy_id'
    # TODO company__user ?!
    success_url = reverse_lazy('portal:my_vacancies')
    success_message = 'Вакансия удалена успешно.'


class MyResumes(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'portal/account/my_resumes.html'
    permission_required = 'portal.add_resume'

    def get_context_data(self, **kwargs):
        context = super(MyResumes, self).get_context_data(**kwargs)
        context.update(
            {'resumes': Resume.objects.filter(user=self.request.user),
             'left_menu': 'my_resumes'}
        )
        return context


@login_required
def resume_detail(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    vacancies = Vacancy.published.filter(company__user=request.user)
    res_feed = FeedbackAndSuggestion.objects.filter(resume=resume)
    vacancies = vacancies.exclude(suggestions__in=res_feed)
    if request.method == 'POST':
        vacancy = get_object_or_404(Vacancy,
                                    pk=request.POST.get('active_vacancy'))
        FeedbackAndSuggestion.objects.create(vacancy=vacancy, resume=resume,
                                             status='invite')
        messages.success(request, 'Приглашение успешно отправлено.')
        return redirect('portal:resume_detail', resume_id=resume_id)
    return render(request, 'portal/account/resume_detail.html',
                  {'resume': resume, 'vacancies': vacancies})


@login_required
@permission_required('portal.add_resume')
def add_resume(request):
    queryset = request.user.experiences.all()
    exp_formset = ExperienceFormSet(queryset=queryset)
    if request.method == 'POST':
        resume_form = ResumeAddForm(request.POST)
        formset = ExperienceFormSet(request.POST, queryset=queryset)
        if resume_form.is_valid() and formset.is_valid():
            new_resume = resume_form.save(commit=False)
            formset.save(commit=False)
            for form in formset:
                if form.cleaned_data:
                    new_exp = form.save(commit=False)
                    new_exp.user = request.user
                    new_exp.save()
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
                   'exp_formset': exp_formset})


@login_required
@permission_required('portal.change_resume')
def edit_resume(request, resume_id):
    edit_res = get_object_or_404(Resume, pk=resume_id, user=request.user)
    comment = edit_res.comment
    queryset = request.user.experiences.all()
    exp_formset = ExperienceFormSet(queryset=queryset)
    if request.method == 'POST':
        resume_form = ResumeAddForm(instance=edit_res, data=request.POST)
        formset = ExperienceFormSet(request.POST, queryset=queryset)
        if resume_form.is_valid() and formset.is_valid():
            new_resume = resume_form.save(commit=False)
            formset.save(commit=False)
            for form in formset:
                if form.cleaned_data:
                    new_exp = form.save(commit=False)
                    new_exp.user = request.user
                    new_exp.save()
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
                  {'resume_form': resume_form,
                   'comment': comment, 'exp_formset': exp_formset})


class DeleteResume(LoginRequiredMixin, PermissionRequiredMixin,
                   SuccessMessageMixin, DeleteView):
    template_name = 'portal/account/delete_resume.html'
    permission_required = 'portal.delete_resume'
    model = Resume
    pk_url_kwarg = 'resume_id'
    success_url = reverse_lazy('portal:my_resumes')
    success_message = 'Резюме удалено успешно.'


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


class FindResume(LoginRequiredMixin, SearchResultsList):
    model = Resume
    context_object_name = "resume"
    template_name = "portal/account/find_resume.html"
    vector = ["title", "salary"]
    headline_expression = Concat(F("id"), F("title"), F("salary"),
                                 F("about_me"))
    annotate_expression = Concat('user_id__username', Value(''))


class FindJob(LoginRequiredMixin, SearchResultsList):
    model = Vacancy
    context_object_name = "job"
    template_name = "portal/account/find_job.html"
    vector = ["title", "salary"]
    headline_expression = Concat(F("id"), F("title"), F("salary"),
                                 F("description"), F("address"))
    annotate_expression = Concat('company_id__title', Value(''))


@login_required()
def feedback_list(request):
    if request.user.has_perm('portal.add_resume'):
        feedbacks = FeedbackAndSuggestion.objects.filter(
            resume__user=request.user)
    else:
        feedbacks = FeedbackAndSuggestion.objects.filter(
            vacancy__company__user=request.user)
    return render(request, 'portal/account/feedback_list.html',
                  {'feedbacks': feedbacks, 'left_menu': 'feed'})


@login_required()
def feedback_detail(request, feedback_id):
    feed = get_object_or_404(FeedbackAndSuggestion, pk=feedback_id)
    feed_messages = feed.messages.all().order_by('-created')
    if request.method == 'POST':
        mes_text = request.POST.get('message_copy').strip() if \
            request.POST.get('message_copy') else None
        if 'invite' in request.POST:
            if mes_text:
                Message.objects.create(text=mes_text, feedback=feed,
                                       sender=request.user)
            feed.status = 'invite'
            feed.save()
        elif 'failure' in request.POST:
            if mes_text:
                Message.objects.create(text=mes_text, feedback=feed,
                                       sender=request.user)
            feed.status = 'failure'
            feed.save()
        elif 'send' in request.POST:
            message_form = MessageForm(request.POST)
            if message_form.is_valid():
                message = message_form.save(commit=False)
                message.feedback = feed
                message.sender = request.user
                message.save()
                messages.success(request, 'Сообщение отослано успешно')
        else:
            if mes_text:
                Message.objects.create(text=mes_text, feedback=feed,
                                       sender=request.user)
            feed.status = 'viewed'
            feed.save()
        return redirect('portal:feedback_list')
    else:
        message_form = MessageForm()
    return render(request, 'portal/account/feedback_detail.html',
                  {'feedback': feed, 'feed_messages': feed_messages,
                   'message_form': message_form})
