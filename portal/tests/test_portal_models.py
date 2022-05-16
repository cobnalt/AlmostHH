from datetime import (
    datetime,
    timedelta,
)

from django.test import TestCase
from django.contrib.auth.models import User

from portal.models import (
    CompanyCard,
    Experience,
    FeedbackAndSuggestion,
    Message,
    Profile,
    Resume,
    Vacancy,
)


class ModelsInstancesForTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            id=1,
            username='SomeUsername',
            first_name='FirstName',
            last_name='LastName',
            email='example@mail.ru',
        )
        CompanyCard.objects.create(
            id=1,
            title='Some Title',
            slug='some-title',
            description='Some description for card',
            user=User.objects.get(id=1),
        )
        Vacancy.objects.create(
            id=1,
            title='Some Title',
            slug='some-title',
            salary=33333,
            company=CompanyCard.objects.get(id=1),
            description='Some description for card',
            address='Some address',
            comment='Some comment',
        )
        Resume.objects.create(
            id=1,
            title='Some Title',
            slug='some-title',
            salary=33333,
            user=User.objects.get(id=1),
            employment='Some employment',
            schedule='Some schedule',
            about_me='Some info about_me',
            education='Some education',
            citizenship='Some citizenship',
            comment='Some comment',
        )
        Experience.objects.create(
            id=1,
            start=datetime.now() - timedelta(344),
            finish=datetime.now() - timedelta(37),
            untilnow=False,
            organisation_name='Some name',
            position='junior assistant of junior assistant',
            function='assist',
            user=User.objects.get(id=1),
        )
        Profile.objects.create(
            id=1,
            user=User.objects.get(id=1),
            contact='Some contact',
            living_city='Some living city',
        )
        FeedbackAndSuggestion.objects.create(
            id=1,
            vacancy=Vacancy.objects.get(id=1),
            resume=Resume.objects.get(id=1),
        )
        Message.objects.create(
            id=1,
            text='Some text',
            sender=User.objects.get(id=1),
            feedback=FeedbackAndSuggestion.objects.get(id=1),
        )


class CompanyCardModelTest(ModelsInstancesForTests):
    def test_title_label(self):
        card = CompanyCard.objects.get(id=1)
        field_label = card._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Наименование')

    def test_title_max_length(self):
        card = CompanyCard.objects.get(id=1)
        field_max_length = card._meta.get_field('title').max_length
        self.assertEquals(field_max_length, 100)

    def test_slug_label(self):
        card = CompanyCard.objects.get(id=1)
        field_label = card._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Слаг')

    def test_slug_max_length(self):
        card = CompanyCard.objects.get(id=1)
        field_max_length = card._meta.get_field('slug').max_length
        self.assertEquals(field_max_length, 100)

    def test_description_label(self):
        card = CompanyCard.objects.get(id=1)
        field_label = card._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание')

    def test_description_max_length(self):
        card = CompanyCard.objects.get(id=1)
        field_max_length = card._meta.get_field('description').max_length
        self.assertEquals(field_max_length, 700)

    def test_logo_label(self):
        card = CompanyCard.objects.get(id=1)
        field_label = card._meta.get_field('logo').verbose_name
        self.assertEquals(field_label, 'Лого')

    def test_contact_label(self):
        card = CompanyCard.objects.get(id=1)
        field_label = card._meta.get_field('contact').verbose_name
        self.assertEquals(field_label, 'Контакты')

    def test_contact_max_length(self):
        card = CompanyCard.objects.get(id=1)
        field_max_length = card._meta.get_field('contact').max_length
        self.assertEquals(field_max_length, 200)

    def test_status_label(self):
        card = CompanyCard.objects.get(id=1)
        field_label = card._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'Статус')

    def test_status_max_length(self):
        card = CompanyCard.objects.get(id=1)
        field_max_length = card._meta.get_field('status').max_length
        self.assertEquals(field_max_length, 15)

    def test_object_repr(self):
        card = CompanyCard.objects.get(id=1)
        expected_object_name = card.title
        self.assertEquals(expected_object_name, str(card))


class VacancyModelTest(ModelsInstancesForTests):
    def test_title_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Наименование')

    def test_title_max_length(self):
        vacancy = Vacancy.objects.get(id=1)
        field_max_length = vacancy._meta.get_field('title').max_length
        self.assertEquals(field_max_length, 100)

    def test_slug_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Слаг')

    def test_slug_max_length(self):
        vacancy = Vacancy.objects.get(id=1)
        field_max_length = vacancy._meta.get_field('slug').max_length
        self.assertEquals(field_max_length, 100)

    def test_salary_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('salary').verbose_name
        self.assertEquals(field_label, 'Зарплата')

    def test_salary_default_value(self):
        vacancy = Vacancy.objects.get(id=1)
        field_default_value = vacancy._meta.get_field('salary').default
        self.assertEquals(field_default_value, 0)

    def test_company_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('company').verbose_name
        self.assertEquals(field_label, 'Компания')

    def test_description_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'Описание вакансии')

    def test_address_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('address').verbose_name
        self.assertEquals(field_label, 'Адрес вакансии')

    def test_address_max_length(self):
        vacancy = Vacancy.objects.get(id=1)
        field_max_length = vacancy._meta.get_field('address').max_length
        self.assertEquals(field_max_length, 200)

    def test_comment_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('comment').verbose_name
        self.assertEquals(field_label, 'Комментарий')

    def test_status_label(self):
        vacancy = Vacancy.objects.get(id=1)
        field_label = vacancy._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'Статус')

    def test_status_max_length(self):
        vacancy = Vacancy.objects.get(id=1)
        field_max_length = vacancy._meta.get_field('status').max_length
        self.assertEquals(field_max_length, 15)

    def test_object_repr(self):
        vacancy = Vacancy.objects.get(id=1)
        expected_object_name = vacancy.title
        self.assertEquals(expected_object_name, str(vacancy))


class ResumeModelTest(ModelsInstancesForTests):
    def test_title_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'Наименование вакансии')

    def test_title_max_length(self):
        resume = Resume.objects.get(id=1)
        field_max_length = resume._meta.get_field('title').max_length
        self.assertEquals(field_max_length, 100)

    def test_slug_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('slug').verbose_name
        self.assertEquals(field_label, 'Слаг')

    def test_slug_max_length(self):
        resume = Resume.objects.get(id=1)
        field_max_length = resume._meta.get_field('slug').max_length
        self.assertEquals(field_max_length, 100)

    def test_salary_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('salary').verbose_name
        self.assertEquals(field_label, 'Зарплата')

    def test_salary_default_value(self):
        resume = Resume.objects.get(id=1)
        field_default_value = resume._meta.get_field('salary').default
        self.assertEquals(field_default_value, 0)

    def test_employment_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('employment').verbose_name
        self.assertEquals(field_label, 'Занятость')

    def test_employment_length(self):
        resume = Resume.objects.get(id=1)
        field_max_length = resume._meta.get_field('employment').max_length
        self.assertEquals(field_max_length, 150)

    def test_schedule_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('schedule').verbose_name
        self.assertEquals(field_label, 'График работы')

    def test_schedule_length(self):
        resume = Resume.objects.get(id=1)
        field_max_length = resume._meta.get_field('schedule').max_length
        self.assertEquals(field_max_length, 150)

    def test_about_me_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('about_me').verbose_name
        self.assertEquals(field_label, 'Обо мне')

    def test_education_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('education').verbose_name
        self.assertEquals(field_label, 'Образование')

    def test_language_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('language').verbose_name
        self.assertEquals(field_label, 'Знание языков')

    def test_language_length(self):
        resume = Resume.objects.get(id=1)
        field_max_length = resume._meta.get_field('language').max_length
        self.assertEquals(field_max_length, 200)

    def test_citizenship_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('citizenship').verbose_name
        self.assertEquals(field_label, 'Гражданство')

    def test_citizenship_length(self):
        resume = Resume.objects.get(id=1)
        field_max_length = resume._meta.get_field('citizenship').max_length
        self.assertEquals(field_max_length, 50)

    def test_comment_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('comment').verbose_name
        self.assertEquals(field_label, 'Комментарий')

    def test_status_label(self):
        resume = Resume.objects.get(id=1)
        field_label = resume._meta.get_field('status').verbose_name
        self.assertEquals(field_label, 'Статус')

    def test_status_max_length(self):
        resume = Resume.objects.get(id=1)
        field_max_length = resume._meta.get_field('status').max_length
        self.assertEquals(field_max_length, 15)

    def test_object_repr(self):
        resume = Resume.objects.get(id=1)
        expected_object_name = resume.title
        self.assertEquals(expected_object_name, str(resume))


class ExperienceModelTest(ModelsInstancesForTests):
    def test_start_label(self):
        exp = Experience.objects.get(id=1)
        field_label = exp._meta.get_field('start').verbose_name
        self.assertEquals(field_label, 'Начало работы')

    def test_finish_label(self):
        exp = Experience.objects.get(id=1)
        field_label = exp._meta.get_field('finish').verbose_name
        self.assertEquals(field_label, 'Окончание работы')

    def test_untilnow_label(self):
        exp = Experience.objects.get(id=1)
        field_label = exp._meta.get_field('untilnow').verbose_name
        self.assertEquals(field_label, 'До настоящего времени')

    def test_organisation_name_label(self):
        exp = Experience.objects.get(id=1)
        field_label = exp._meta.get_field('organisation_name').verbose_name
        self.assertEquals(field_label, 'Наименование организации')

    def test_organisation_name_max_length(self):
        exp = Experience.objects.get(id=1)
        field_length = exp._meta.get_field('organisation_name').max_length
        self.assertEquals(field_length, 100)

    def test_position_label(self):
        exp = Experience.objects.get(id=1)
        field_label = exp._meta.get_field('position').verbose_name
        self.assertEquals(field_label, 'Должность')

    def test_position_max_length(self):
        exp = Experience.objects.get(id=1)
        field_length = exp._meta.get_field('position').max_length
        self.assertEquals(field_length, 100)

    def test_function_label(self):
        exp = Experience.objects.get(id=1)
        field_label = exp._meta.get_field('function').verbose_name
        self.assertEquals(field_label, 'Обязанности')

    def test_user_label(self):
        exp = Experience.objects.get(id=1)
        field_label = exp._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')


class ProfileModelTest(ModelsInstancesForTests):
    def test_user_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'Пользователь')

    def test_photo_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('photo').verbose_name
        self.assertEquals(field_label, 'Фото')

    def test_date_of_birth_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('date_of_birth').verbose_name
        self.assertEquals(field_label, 'Дата рождения')

    def test_contact_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('contact').verbose_name
        self.assertEquals(field_label, 'Контакты')

    def test_contact_max_length(self):
        profile = Profile.objects.get(id=1)
        field_length = profile._meta.get_field('contact').max_length
        self.assertEquals(field_length, 200)

    def test_living_city_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('living_city').verbose_name
        self.assertEquals(field_label, 'Город проживания')

    def test_living_city_max_length(self):
        profile = Profile.objects.get(id=1)
        field_length = profile._meta.get_field('living_city').max_length
        self.assertEquals(field_length, 50)

    def test_sex_label(self):
        profile = Profile.objects.get(id=1)
        field_label = profile._meta.get_field('sex').verbose_name
        self.assertEquals(field_label, 'Пол')

    def test_sex_max_length(self):
        profile = Profile.objects.get(id=1)
        field_length = profile._meta.get_field('sex').max_length
        self.assertEquals(field_length, 15)

    def test_object_repr(self):
        profile = Profile.objects.get(id=1)
        expected_object_name = f'Профиль для пользователя {profile.user.username}'
        self.assertEquals(expected_object_name, str(profile))


class FeedbackAndSuggestionModelTest(ModelsInstancesForTests):
    def test_vacancy_label(self):
        feedback_and_suggestion = FeedbackAndSuggestion.objects.get(id=1)
        field_label = feedback_and_suggestion._meta.get_field('vacancy').verbose_name
        self.assertEquals(field_label, 'Вакансия')

    def test_resume_label(self):
        feedback_and_suggestion = FeedbackAndSuggestion.objects.get(id=1)
        field_label = feedback_and_suggestion._meta.get_field('resume').verbose_name
        self.assertEquals(field_label, 'Резюме')

    def test_object_repr(self):
        feedback_and_suggestion = FeedbackAndSuggestion.objects.get(id=1)
        expected_object_name = f'Feedback {feedback_and_suggestion.id}'
        self.assertEquals(expected_object_name, str(feedback_and_suggestion))


class MessageModelTest(ModelsInstancesForTests):
    def test_text_label(self):
        message = Message.objects.get(id=1)
        field_label = message._meta.get_field('text').verbose_name
        self.assertEquals(field_label, 'Текст')

    def test_text_length(self):
        message = Message.objects.get(id=1)
        field_length = message._meta.get_field('text').max_length
        self.assertEquals(field_length, 1000)

    def test_sender_label(self):
        message = Message.objects.get(id=1)
        field_label = message._meta.get_field('sender').verbose_name
        self.assertEquals(field_label, 'Отправитель')

    def test_feedback_label(self):
        message = Message.objects.get(id=1)
        field_label = message._meta.get_field('feedback').verbose_name
        self.assertEquals(field_label, 'Отклик')

    def test_object_repr(self):
        message = Message.objects.get(id=1)
        expected_object_name = f'Message {message.id}'
        self.assertEquals(expected_object_name, str(message))
