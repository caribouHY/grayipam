from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from network.forms import LoginForm


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'network/index.html'


class Login(LoginView):
    template_name = 'network/login.html'
    form_class = LoginForm


class Logout(LogoutView):
    template_name = 'network/login.html'
