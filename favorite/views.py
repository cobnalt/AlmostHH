from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from portal.models import Resume, Vacancy
from django.views.generic import CreateView, DetailView, TemplateView, ListView

from django.contrib.auth.mixins import LoginRequiredMixin

# TODO на уровне моделей реализовать?
class SessionHandlerMixin():
    SLANG = {'response_key': 'favorites',
             'key_word': 'type',
             'model_key': 'id'}

    def __call__(self, *args):
        response, model, key_word = args
        result = response.get(self.SLANG['response_key'])
        if result:
            result = filter(lambda x: x[self.SLANG['key_word']] == key_word, result)

        return [get_object_or_404(model, pk=item[self.SLANG['model_key']])
                  for item in result] if result else None


class FavoritesList(LoginRequiredMixin, SessionHandlerMixin, TemplateView):
    template_name = 'favorite/favorites_list.html'

    def get(self, request, *args, **kwargs):
        resume = self.__call__(request.session, Resume, 'res')
        vacancy = self.__call__(request.session, Vacancy, 'vac')

        return render(request, self.template_name,
                      {'res': resume, 'vac': vacancy, 'left_menu': 'favs'})


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


@login_required()
def add_to_favorites(request):
    if request.method == 'POST':
        if not request.session.get('favorites'):
            request.session['favorites'] = list()
        else:
            request.session['favorites'] = list(request.session['favorites'])

        item_exist = next((item for item in request.session['favorites'] if
                           item['type'] == request.POST.get('type') and item[
                               'id'] == request.POST.get('id')), False)

        add_data = {
            'type': request.POST.get('type'),
            'id': request.POST.get('id'),
        }

        if not item_exist:
            request.session['favorites'].append(add_data)
            request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'type': request.POST.get('type'),
            'id': request.POST.get('id'),
            'count': len(request.session['favorites']),
        }
        request.session.modified = True
        return JsonResponse(data)

    return redirect(request.POST.get('url_from'))


@login_required()
def remove_from_favorites(request):
    if request.method == 'POST':
        for item in request.session['favorites']:
            if item['type'] == request.POST.get('type') and item[
                'id'] == request.POST.get('id'):
                item.clear()

        while {} in request.session['favorites']:
            request.session['favorites'].remove({})

        if not request.session['favorites']:
            del request.session['favorites']

        request.session.modified = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = {
            'type': request.POST.get('type'),
            'id': request.POST.get('id'),
            'count': 0 if not request.session.get('favorites')
            else len(request.session['favorites']),
        }
        request.session.modified = True
        return JsonResponse(data)

    return redirect(request.POST.get('url_from'))


@login_required()
def favorites_api(request):
    return JsonResponse(request.session.get('favorites'), safe=False)
