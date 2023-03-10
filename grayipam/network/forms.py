from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Network, Host


class MyModelForm(ModelForm):
    template_name_p = 'boot_form.html'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            # print(field.widget.is_required)
            field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
            field.widget.attrs['size'] = 32


class NetworkForm(MyModelForm):

    class Meta:
        model = Network
        fields = ['name', 'ipv4_cidr', 'vid', 'note']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['vid'].widget.attrs['max'] = 0xfff
        self.fields['vid'].widget.attrs['min'] = 0


class HostForm(MyModelForm):

    class Meta:
        model = Host
        fields = ['network', 'ipv4', 'hostname']
