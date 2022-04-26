from django import template
from ..models import Resume, Vacancy, FeedbackAndSuggestion

register = template.Library()


@register.simple_tag
def total_resumes(user):
    return Resume.objects.filter(user=user).count()


@register.simple_tag
def total_vacancies(user):
    return Vacancy.objects.filter(company__user=user).count()


@register.simple_tag
def total_feeds(user):
    if user.has_perm('portal.add_resume'):
        return FeedbackAndSuggestion.objects.filter(resume__user=user).count()
    else:
        return FeedbackAndSuggestion.objects.filter(
            vacancy__company__user=user).count()
