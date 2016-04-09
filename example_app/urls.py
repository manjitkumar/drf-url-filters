from django.conf.urls import include, url

from rest_framework.routers import DefaultRouter
from example_app.views import PlayersViewSet, TeamsViewSet


# Create a router and register our viewsets with it.
router = DefaultRouter()

router.register(r'players', PlayersViewSet, base_name='players')
router.register(r'teams', TeamsViewSet, base_name='teams')

urlpatterns = [
    url(r'^api/', include(router.urls)),
]
