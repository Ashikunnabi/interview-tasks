from django.shortcuts import render
from django.views.generic import TemplateView


class UserView(TemplateView):
    template_name = 'user/user.html'
