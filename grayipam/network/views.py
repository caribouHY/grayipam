from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from .forms import LoginForm, NetworkForm, HostForm
from .models import Network, Host


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

    def get_context_data(self, **kwargs):
        if 'host_form' not in kwargs:
            form = HostForm(initial={'network': self.object})
            from django.forms import HiddenInput
            form.fields['network'].widget = HiddenInput()
            kwargs['host_form'] = form
        return super().get_context_data(**kwargs)


class NetworkDelete(LoginRequiredMixin, DeleteView):
    model = Network
    http_method_names = ['post']
    success_url = reverse_lazy('network:network_list')


class HostCreate(LoginRequiredMixin, CreateView):
    template_name = 'network/form_error.html'
    model = Host
    form_class = HostForm
    http_method_names = ['post']

    def get_context_data(self, **kwargs):
        if "next_url" not in kwargs:
            kwargs["next_url"] = reverse_lazy(
                'network:network_detail', kwargs={"pk": self.kwargs["pk"]})
        return super().get_context_data(**kwargs)
