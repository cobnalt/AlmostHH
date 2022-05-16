from django.test import TestCase

from portal.forms import (
    LoginForm,
    UserRegistrationForm,
    VacancyAddForm,
    UserEditForm,
    CompanyCardEditForm,
    ProfileEditForm,
    ResumeAddForm,
    ExperienceAddForm,
    MessageForm,
)


def parse_errors(errors):
    return [f'{field} - {exception.as_text()[2:-1]}' for field, exception in errors.items()]


class LoginFormTest(TestCase):
    def setUp(self):
        self.form = LoginForm()

    def test_form_username_label(self):
        form_field_label = self.form.fields['username'].label
        self.assertIsNone(form_field_label)

    def test_form_password_label(self):
        form_field_label = self.form.fields['password'].label
        self.assertIsNone(form_field_label)

    def test_form_valid(self):
        form = LoginForm(
            data={
                'username': 'some_username',
                'password': 'password',
            },
        )
        self.assertTrue(form.is_valid(), parse_errors(form.errors))

    def test_form_invalid(self):
        test_cases = [
            {
                'password': 'password',
            },
            {
                'username': 'some_username',
            },
            {
            },
        ]
        for idx, el in enumerate(test_cases):
            form = LoginForm(data=el)
            self.assertFalse(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')


class UserRegistrationFormTest(TestCase):
    def setUp(self):
        self.form = UserRegistrationForm()

    def test_form_password_label(self):
        form_field_label = self.form.fields['password'].label
        self.assertEquals(form_field_label, 'Пароль')

    def test_form_password2_label(self):
        form_field_label = self.form.fields['password2'].label
        self.assertEquals(form_field_label, 'Повторите пароль')

    def test_form_role_label(self):
        form_field_label = self.form.fields['role'].label
        self.assertEquals(form_field_label, 'Роль')

    def test_form_valid(self):
        test_cases = [
            {
                'username': 'some_username',
                'first_name': 'some_first_name',
                'email': 'example@mail.ru',
                'password': 'password',
                'password2': 'password',
                'role': 'W',
            },
            {
                'username': 'some_username',
                'email': 'example@mail.ru',
                'password': 'password',
                'password2': 'password',
                'role': 'W',
            },
            {
                'username': 'some_username',
                'password': 'password',
                'password2': 'password',
                'role': 'W',
            },
        ]

        for idx, el in enumerate(test_cases):
            form = UserRegistrationForm(data=el)
            self.assertTrue(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')

    def test_form_invalid(self):
        test_cases = [
            {
                'password': 'password',
                'password2': 'password',
                'role': 'W',
            },
            {
                'username': 'some_username',
                'password': 'password',
                'password2': 'password',
            },
            {
            },
        ]

        for idx, el in enumerate(test_cases):
            form = UserRegistrationForm(data=el)
            self.assertFalse(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')

    def test_form_invalid_passwords(self):
        form = UserRegistrationForm(
            data={
                'username': 'some_username',
                'first_name': 'some_first_name',
                'email': 'example@mail.ru',
                'password': 'some_pass',
                'password2': 'password2',
                'role': 'W',
            },
        )
        self.assertEqual(form.errors, {'password2': ['Пароли не совпадают.']})


class VacancyAddFormTest(TestCase):
    def test_form_valid(self):
        form = VacancyAddForm(
            data={
                'title': 'Some title',
                'salary': 3333333,
                'description': 'Some description',
                'address': 'Some address',
            },
        )
        self.assertTrue(form.is_valid(), parse_errors(form.errors))

    def test_form_invalid(self):
        test_cases = [
            {
                'salary': 'Some salary',
                'description': 'Some description',
                'address': 'Some address',
            },
            {
                'title': 'Some title',
                'description': 'Some description',
                'address': 'Some address',
            },
            {
                'title': 'Some title',
                'salary': 'Some salary',
                'address': 'Some address',
            },
            {
                'title': 'Some title',
                'salary': 'Some salary',
                'description': 'Some description',
            },
            {
            },
        ]
        for idx, el in enumerate(test_cases):
            form = VacancyAddForm(data=el)
            self.assertFalse(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')


class UserEditFormTest(TestCase):
    def test_form_valid(self):
        test_cases = [
            {
                'first_name': 'Some first name',
                'last_name': 'Some last name',
                'email': 'some@mail.ru',
            },
            {
                'last_name': 'Some last name',
                'email': 'some@mail.ru',
            },
            {
                'first_name': 'Some first name',
                'email': 'some@mail.ru',
            },
            {
                'first_name': 'Some first name',
                'last_name': 'Some last name',
            },
            {
            },
        ]
        for idx, el in enumerate(test_cases):
            form = UserEditForm(data=el)
            self.assertTrue(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')


class CompanyCardEditFormTest(TestCase):
    def test_form_valid(self):
        test_cases = [
            {
                'title': 'Some title',
                'description': 'Some description',
                'logo': 'Some logo',
                'contact': 'Some contacts',
            },
            {
                'title': 'Some title',
                'logo': 'Some logo',
                'contact': 'Some contacts',
            },
            {
                'title': 'Some title',
                'description': 'Some description',
                'contact': 'Some contacts',
            },
            {
                'title': 'Some title',
                'description': 'Some description',
                'logo': 'Some logo',
                'contact': 'Some contacts',
            },
            {
                'title': 'Some title',
                'contact': 'Some contacts',
            },
        ]
        for idx, el in enumerate(test_cases):
            form = CompanyCardEditForm(data=el)
            self.assertTrue(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')

    def test_form_invalid(self):
        test_cases = [
            {
                'title': 'Some title',
            },
            {
                'contact': 'Some contacts',
            },
            {
            },
        ]
        for idx, el in enumerate(test_cases):
            form = CompanyCardEditForm(data=el)
            self.assertFalse(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')


class ProfileEditFormTest(TestCase):
    def setUp(self):
        self.form = ProfileEditForm()

    def test_form_date_of_birth_label(self):
        form_field_label = self.form.fields['date_of_birth'].label
        self.assertEqual(form_field_label, 'Дата рождения')

    def test_form_date_of_birth_input_formats(self):
        form_field_input_formats = self.form.fields['date_of_birth'].input_formats
        self.assertEquals(form_field_input_formats, ['%d.%m.%Y'])

    def test_form_valid(self):
        form = ProfileEditForm(
            data={
                'date_of_birth': '17.04.1999',
                'contact': 'Some contacts',
                'living_city': 'Some city',
                'sex': 'male',
            },
        )
        self.assertTrue(form.is_valid(), parse_errors(form.errors))

    def test_form_invalid(self):
        test_cases = [
            {
                'contact': 'Some contacts',
                'living_city': 'Some city',
                'sex': 'male',
            },
            {
                'date_of_birth': '17.04.1999',
                'living_city': 'Some city',
                'sex': 'male',
            },
            {
                'date_of_birth': '17.04.1999',
                'contact': 'Some contacts',
                'sex': 'male',
            },
            {
                'date_of_birth': '17.04.1999',
                'contact': 'Some contacts',
                'living_city': 'Some city',
            },
            {
            },
        ]
        for idx, el in enumerate(test_cases):
            form = ProfileEditForm(data=el)
            self.assertFalse(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')


class ResumeAddFormTest(TestCase):
    def test_form_valid(self):
        form = ResumeAddForm(
            data={
                'title': 'Some title',
                'salary': 3333333,
                'employment': 'Some employment',
                'schedule': 'Some schedule',
                'about_me': 'Something about_me',
                'education': 'Some education',
                'language': 'Some language',
                'citizenship': 'Some citizenship',
            },
        )
        self.assertTrue(form.is_valid(), parse_errors(form.errors))

    def test_form_invalid(self):
        test_cases = [
            {
                'salary': 'Some salary',
                'employment': 'Some employment',
                'schedule': 'Some schedule',
                'about_me': 'Something about_me',
                'education': 'Some education',
                'language': 'Some language',
                'citizenship': 'Some citizenship',
            },
            {
                'title': 'Some title',
                'employment': 'Some employment',
                'schedule': 'Some schedule',
                'about_me': 'Something about_me',
                'education': 'Some education',
                'language': 'Some language',
                'citizenship': 'Some citizenship',
            },
            {
                'title': 'Some title',
                'salary': 'Some salary',
                'schedule': 'Some schedule',
                'about_me': 'Something about_me',
                'education': 'Some education',
                'language': 'Some language',
                'citizenship': 'Some citizenship',
            },
            {
                'title': 'Some title',
                'salary': 'Some salary',
                'employment': 'Some employment',
                'about_me': 'Something about_me',
                'education': 'Some education',
                'language': 'Some language',
                'citizenship': 'Some citizenship',
            },
            {
                'title': 'Some title',
                'salary': 'Some salary',
                'employment': 'Some employment',
                'schedule': 'Some schedule',
                'education': 'Some education',
                'language': 'Some language',
                'citizenship': 'Some citizenship',
            },
            {
                'title': 'Some title',
                'salary': 'Some salary',
                'employment': 'Some employment',
                'schedule': 'Some schedule',
                'about_me': 'Something about_me',
                'language': 'Some language',
                'citizenship': 'Some citizenship',
            },
            {
                'title': 'Some title',
                'salary': 'Some salary',
                'employment': 'Some employment',
                'schedule': 'Some schedule',
                'about_me': 'Something about_me',
                'education': 'Some education',
                'citizenship': 'Some citizenship',
            },
            {
                'title': 'Some title',
                'salary': 'Some salary',
                'employment': 'Some employment',
                'schedule': 'Some schedule',
                'about_me': 'Something about_me',
                'education': 'Some education',
                'language': 'Some language',
            },
            {
            },
        ]
        for idx, el in enumerate(test_cases):
            form = ResumeAddForm(data=el)
            self.assertFalse(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')


class ExperienceAddFormTest(TestCase):
    def setUp(self):
        self.form = ExperienceAddForm()

    def test_form_start_label(self):
        form_field_label = self.form.fields['start'].label
        self.assertEquals(form_field_label, 'Начало')

    def test_form_start_input_formats(self):
        form_field_input_formats = self.form.fields['start'].input_formats
        self.assertEquals(form_field_input_formats, ['%d.%m.%Y'])

    def test_form_finish_label(self):
        form_field_label = self.form.fields['finish'].label
        self.assertEquals(form_field_label, 'Окончание')

    def test_form_finish_input_formats(self):
        form_field_input_formats = self.form.fields['finish'].input_formats
        self.assertEquals(form_field_input_formats, ['%d.%m.%Y'])

    def test_form_valid(self):
        test_cases = [
            {
                'until_now': False,
                'start': '17.04.2018',
                'finish': '21.10.2020',
                'organisation_name': 'Some organisation_name',
                'position': 'Some position',
                'function': 'Some function',
            },
            {
                'until_now': True,
                'start': '17.04.2018',
                'finish': '21.10.2020',
                'organisation_name': 'Some organisation_name',
                'position': 'Some position',
                'function': 'Some function',
            },
            {
                'start': '17.04.2018',
                'finish': '21.10.2020',
                'organisation_name': 'Some organisation_name',
                'position': 'Some position',
                'function': 'Some function',
            },
        ]

        for idx, el in enumerate(test_cases):
            form = ExperienceAddForm(data=el)
            self.assertTrue(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')

    def test_form_invalid(self):
        test_cases = [
            {
                'finish': '21.10.2020',
                'organisation_name': 'Some organisation_name',
                'position': 'Some position',
                'function': 'Some function',
            },
            {
                'start': '17.04.2018',
                'finish': '21.10.2020',
                'organisation_name': 'Some organisation_name',
                'position': 'Some position',
                'function': 'Some function',
            },
            {
                'start': '17.04.2018',
                'finish': '21.10.2020',
                'organisation_name': 'Some organisation_name',
                'position': 'Some position',
                'function': 'Some function',
            },
            {
                'start': '17.04.2018',
                'finish': '21.10.2020',
                'organisation_name': 'Some organisation_name',
                'position': 'Some position',
                'function': 'Some function',
            },
            {
            },
        ]
        for idx, el in enumerate(test_cases):
            form = ProfileEditForm(data=el)
            self.assertFalse(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')


class MessageFormTest(TestCase):
    def setUp(self):
        self.form = MessageForm()

    def test_form_text_label(self):
        form_field_label = self.form.fields['text'].label
        self.assertEquals(form_field_label, 'Текст сообщения')

    def test_form_valid(self):
        test_cases = [
            {
                'text': 'Some text',
            },
            {
            },
        ]
        for idx, el in enumerate(test_cases):
            form = MessageForm(data=el)
            self.assertTrue(form.is_valid(), f'test_{idx + 1}, {parse_errors(form.errors)}')
