from django.urls import path, include
from .views import UserView

urlpatterns = [
    path('api/', include('user.api.urls')),
    path('', UserView.as_view(), name='users'),
]
