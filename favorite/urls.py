from django.urls import path

from . import views
from favorite.views import FavoritesList

app_name = 'favorites'

urlpatterns = [
    # path('', views.favorites_list, name='favorites_list'),
    path('', FavoritesList.as_view(), name='favorites_list'),
    path('add/', views.add_to_favorites, name='add'),
    path('remove/', views.remove_from_favorites, name='remove'),
    path('api/', views.favorites_api, name='api'),
]
