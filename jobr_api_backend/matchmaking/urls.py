from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MatchViewSet, ApplyVacancyViewSet

router = DefaultRouter()
router.register('matches', MatchViewSet, basename='match')
router.register('applications', ApplyVacancyViewSet, basename='application')

urlpatterns = [
    path('', include(router.urls)),
]
