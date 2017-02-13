"""Views for CFN."""
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'cfn/home.html'
