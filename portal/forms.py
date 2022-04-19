from django import forms
from django.contrib.auth.models import User
from .models import CompanyCard, Vacancy, Profile, Resume, Experience, Message


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    role_choice = (('W', 'Соискатель'), ('E', 'Работодатель'))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)
    role = forms.ChoiceField(label='Роль', choices=role_choice)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class VacancyAddForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('title', 'salary', 'description', 'address')


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class CompanyCardEditForm(forms.ModelForm):
    class Meta:
        model = CompanyCard
        fields = ('title', 'description', 'logo', 'contact')


class ProfileEditForm(forms.ModelForm):
    date_of_birth = forms.DateField(input_formats=['%d.%m.%Y'])

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo', 'contact', 'living_city', 'sex')


class ResumeAddForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ('title', 'salary', 'employment', 'schedule', 'about_me',
                  'education', 'language', 'citizenship')


class ExperienceAddForm(forms.ModelForm):
    start = forms.DateField(input_formats=['%d.%m.%Y'], label='Начало')
    finish = forms.DateField(input_formats=['%d.%m.%Y'], label='Окончание')

    class Meta:
        model = Experience
        fields = ('until_now', 'finish', 'start', 'organisation_name',
                  'position', 'function')


ExperienceFormSet = forms.modelformset_factory(Experience,
                                               form=ExperienceAddForm,
                                               can_delete=True,
                                               extra=1)


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)
        labels = {'text': 'Текст сообщения'}
        widgets = {'text': forms.widgets.Textarea(attrs={'class': 'form-control',
                                                         'rows': 3})}
