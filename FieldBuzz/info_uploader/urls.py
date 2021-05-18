from django.urls import path
from .views import PersonalInformationView

urlpatterns = [
    path('', PersonalInformationView.as_view(), name='personal_information'),
]
