from django.urls import include, path
from rest_framework import routers
from . import viewsets

router = routers.DefaultRouter()
router.register(r'users', viewsets.UserViewSet)

# Wire up our API using automatic URL routing.
urlpatterns = [
    path('', include(router.urls))
]
