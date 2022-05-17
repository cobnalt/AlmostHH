from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from portal.models import Resume, Vacancy
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin


class FavoritesList(LoginRequiredMixin, TemplateView):
    template_name = 'favorite/favorites_list.html'

    def get_context_data(self, **kwargs):
        session = self.request.session.get('favorites')
        session = [] if not session else session

        context = super(FavoritesList, self).get_context_data(**kwargs)
        context.update(
            {'res': [get_object_or_404(Resume, pk=item['id']) for item
                     in filter(lambda x: x['type'] == 'res', session)],
             'vac': [get_object_or_404(Vacancy, pk=item['id']) for item
                     in filter(lambda x: x['type'] == 'vac', session)],
             'left_menu': 'favs'
             })
        return context


class AddToFavorites(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        sequence = dict(type=self.request.POST.get('type'),
                        id=self.request.POST.get('id'))
        session = self.request.session.get('favorites')

        session = [] if not session else session

        if sequence not in session:
            session.append(sequence)

            self.request.session.update({'favorites': session})
            self.request.session.modified = True

            sequence.update({'count': len(session)})

            return JsonResponse(sequence)


class RemoveFromFavorites(LoginRequiredMixin, TemplateView):
    def post(self, request, *args, **kwargs):
        sequence = dict(type=self.request.POST.get('type'),
                        id=self.request.POST.get('id'))
        session = self.request.session.get('favorites')

        session = [item for item in session if item['id'] != sequence['id']]

        self.request.session.update({'favorites': session})
        self.request.session.modified = True

        sequence.update({'count': len(session)})

        return JsonResponse(sequence)


class FavoritesApi(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(request.session.get('favorites'), safe=False)
