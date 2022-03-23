from django import forms
from django.contrib.auth.models import User
from .models import CompanyCard, Vacancy, Profile


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
            raise forms.ValidationError('Passwords don\'t match.')
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
    date_of_birth = forms.DateField(widget=forms.SelectDateWidget(years=range(1950, 2020)))

    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo', 'contact', 'living_city', 'sex')
