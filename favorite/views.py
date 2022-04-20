from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from portal.models import Resume, Vacancy


@login_required()
def favorites_list(request):
    fav = None if not request.session.get('favorites') else request.session[
        'favorites']
    res = None
    vac = None
    if fav:
        res = [get_object_or_404(Resume, pk=item['id']) for item in
               fav if item['type'] == 'res']
        vac = [get_object_or_404(Vacancy, pk=item['id']) for item in
               fav if item['type'] == 'vac']
    return render(request, 'favorite/favorites_list.html',
                  {'res': res, 'vac': vac})


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
        }
        request.session.modified = True
        return JsonResponse(data)

    return redirect(request.POST.get('url_from'))


@login_required()
def favorites_api(request):
    return JsonResponse(request.session.get('favorites'), safe=False)
