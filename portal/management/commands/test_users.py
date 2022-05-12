from random import randint, randrange, choice, sample, shuffle
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from mimesis import Person, Finance, Text, Address
from mimesis.locales import Locale
from mimesis.enums import Gender
from portal.models import CompanyCard, Vacancy, Resume, Profile


class Command(BaseCommand):
    help = 'Create 10 test users: 5 Workers and 5 Employers'

    employment = ['Полная занятость', 'Частичная занятость',
                  'Проектная работа', 'Стажировка', 'Волонтерство']
    schedule = ['Полный день', 'Сменный график', 'Гибкий график',
                'Удаленная работа', 'Вахтовый метод']
    languages = ['Английский', 'Немецкий', 'Французский', 'Китайский']

    def make_person(self, password=None):
        en_person = Person(Locale.EN)
        ru_person = Person(Locale.RU)
        return (
            en_person.username(mask='l_l_d', drange=(1000, 5000)),
            en_person.email(unique=True),
            password if password else en_person.password(),
            ru_person.first_name(gender=Gender.MALE),
            ru_person.last_name(gender=Gender.MALE),
        )

    def make_company_card(self):
        ru_company = Finance(Locale.RU)
        ru_address = Address(Locale.RU)
        ru_text = Text(Locale.RU)
        return (
            ru_company.company(),
            ru_text.text(quantity=10),
            ru_address.address(),
        )

    def make_profile(self):
        ru_person = Person(Locale.RU)
        ru_address = Address(Locale.RU)
        return (
            ru_person.telephone(),
            ru_address.city(),
        )

    def make_resume(self):
        ru_text = Text(Locale.RU)
        ru_person = Person(Locale.RU)
        shuffle(self.employment)
        employment = ', '.join(sample(self.employment, randint(1, 3)))
        shuffle(self.schedule)
        schedule = ', '.join(sample(self.schedule, randint(1, 3)))
        return (
            ru_text.text(quantity=10),
            choice(self.languages),
            employment,
            schedule,
            ru_person.occupation(),
            randrange(20000, 200000, 5000),
            ru_person.university()
        )

    def make_vacancy(self):
        ru_text = Text(Locale.RU)
        ru_person = Person(Locale.RU)
        ru_address = Address(Locale.RU)
        return (
            ru_person.occupation(),
            randrange(20000, 200000, 5000),
            ru_text.text(quantity=10),
            ru_address.address()
        )

    def handle(self, *args, **options):
        for i in range(1, 11):
            username, email, password, first_name, last_name = self.make_person(password='12345')
            try:
                new_user = User.objects.create_user(
                    username=username, email=email, password=password,
                    first_name=first_name, last_name=last_name)
                if i <= 5:
                    new_user.groups.add(Group.objects.get(name='Workers'))
                    contact, living_city = self.make_profile()
                    Profile.objects.create(user=new_user, contact=contact,
                                           living_city=living_city)
                    for _ in range(10):
                        about_me, language, employment, schedule, title, salary, education = self.make_resume()
                        Resume.objects.create(title=title,
                                              slug=f'resume{randint(1, 100)}',
                                              salary=salary,
                                              user=new_user,
                                              employment=employment,
                                              schedule=schedule,
                                              about_me=about_me,
                                              education=education,
                                              language=language,
                                              citizenship='Россия',
                                              status='published',
                                              )
                else:
                    new_user.groups.add(Group.objects.get(name='Employers'))
                    title, description, contact = self.make_company_card()
                    new_company = CompanyCard.objects.create(title=title, user=new_user,
                                                             description=description,
                                                             contact=contact,
                                                             status='published')
                    for _ in range(10):
                        title, salary, description, address = self.make_vacancy()
                        Vacancy.objects.create(title=title,
                                               slug=f'vacancy{randint(1, 100)}',
                                               salary=salary,
                                               company=new_company,
                                               description=description,
                                               address=address,
                                               status='published',
                                               )
            except Exception:
                raise CommandError("Can't create User")
