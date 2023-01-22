from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .forms import LoginForm, NetworkForm
from .models import Network


def error_404(request, exception):
    return redirect(reverse('network:index'))


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'network/index.html'


class Login(LoginView):
    template_name = 'network/login.html'
    form_class = LoginForm


class Logout(LogoutView):
    template_name = 'network/login.html'


class NetworkList(LoginRequiredMixin, ListView):
    template_name = 'network/network_list.html'
    model = Network


class NetworkCreate(LoginRequiredMixin, CreateView):
    template_name = 'network/network_create.html'
    model = Network
    form_class = NetworkForm
    success_url = reverse_lazy('network:network_list')


class NetworkDetail(LoginRequiredMixin, DetailView):
    template_name = 'network/network_detail.html'
    model = Network


class NetworkDelete(LoginRequiredMixin, DeleteView):
    model = Network
    http_method_names = ['post']
    success_url = reverse_lazy('network:network_list')
