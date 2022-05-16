from django.urls import path

from .views import QuoteList, SearchResultsList

urlpatterns = [
    path(r"", QuoteList.as_view(), name="all_quotes"),
    path(r"search/", SearchResultsList.as_view(), name="search_results"),
]
