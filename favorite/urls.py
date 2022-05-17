from django.urls import path

from . import views
from favorite.views import FavoritesList, AddToFavorites, RemoveFromFavorites, FavoritesApi

app_name = 'favorites'

urlpatterns = [
    path('', FavoritesList.as_view(), name='favorites_list'),
    path(r'add/', AddToFavorites.as_view(), name='add'),
    path(r'remove/', RemoveFromFavorites.as_view(), name='remove'),
    path(r'api/', FavoritesApi.as_view(), name='api'),
]
