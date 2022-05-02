from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from portal.models import Resume, Vacancy
from django.views.generic import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin


class FavoritesList(LoginRequiredMixin, TemplateView):
    template_name = 'favorite/favorites_list.html'

    def get_context_data(self, **kwargs):
        context = super(FavoritesList, self).get_context_data(**kwargs)
        context.update(
            {'res': [get_object_or_404(Resume, pk=item['id']) for item
                     in filter(lambda x: x['type'] == 'res',
                               self.request.session.get('favorites'))],
             'vac': [get_object_or_404(Resume, pk=item['id']) for item
                     in filter(lambda x: x['type'] == 'vac',
                               self.request.session.get('favorites'))],
             'left_menu': 'favs'
             })
        return context

# @login_required()
# def favorites_list(request):
#     fav = None if not request.session.get('favorites') else request.session[
#         'favorites']
#     res = filter(lambda x: x['type'] == 'res', request.session['favorites'])
#     vac = filter(lambda x: x['type'] == 'vac', request.session['favorites'])
#     if fav:
#         res = [get_object_or_404(Resume, pk=item['id']) for item in
#                res]
#         vac = [get_object_or_404(Vacancy, pk=item['id']) for item in
#                vac]
#     print(res, vac)
#     return render(request, 'favorite/favorites_list.html',
#                   {'res': res, 'vac': vac, 'left_menu': 'favs'})


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


# @login_required()
# def add_to_favorites(request):
#     if request.method == 'POST':
#         if not request.session.get('favorites'):
#             request.session['favorites'] = list()
#         else:
#             request.session['favorites'] = list(request.session['favorites'])
#
#         item_exist = next((item for item in request.session['favorites'] if
#                            item['type'] == request.POST.get('type') and item[
#                                'id'] == request.POST.get('id')), False)
#         print(request.session['favorites'])
#         add_data = {
#             'type': request.POST.get('type'),
#             'id': request.POST.get('id'),
#         }
#
#         if not item_exist:
#             request.session['favorites'].append(add_data)
#             request.session.modified = True
#
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         data = {
#             'type': request.POST.get('type'),
#             'id': request.POST.get('id'),
#             'count': len(request.session['favorites']),
#         }
#         request.session.modified = True
#         return JsonResponse(data)
#
#     return redirect(request.POST.get('url_from'))

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


# @login_required()
# def remove_from_favorites(request):
#     if request.method == 'POST':
#         for item in request.session['favorites']:
#             if item['type'] == request.POST.get('type') and item[
#                 'id'] == request.POST.get('id'):
#                 item.clear()
#
#         while {} in request.session['favorites']:
#             request.session['favorites'].remove({})
#
#         if not request.session['favorites']:
#             del request.session['favorites']
#
#         request.session.modified = True
#
#     if request.headers.get('x-requested-with') == 'XMLHttpRequest':
#         data = {
#             'type': request.POST.get('type'),
#             'id': request.POST.get('id'),
#             'count': 0 if not request.session.get('favorites')
#             else len(request.session['favorites']),
#         }
#         request.session.modified = True
#         return JsonResponse(data)
#
#     return redirect(request.POST.get('url_from'))

class FavoritesApi(LoginRequiredMixin, TemplateView):
    def get(self, request, *args, **kwargs):
        return JsonResponse(request.session.get('favorites'), safe=False)

# @login_required()
# def favorites_api(request):
#     return JsonResponse(request.session.get('favorites'), safe=False)
