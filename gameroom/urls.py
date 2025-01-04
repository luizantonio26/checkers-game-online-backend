
from django.urls import include, path

from gameroom.views.match_view import MatchViewSet

urlpatterns = [
    path('matches/', MatchViewSet.as_view({'get': 'list'})),
]
