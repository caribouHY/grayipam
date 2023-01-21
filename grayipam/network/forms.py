from django.forms import ModelForm, Form
from django.contrib.auth.forms import AuthenticationForm
from .models import Network


class MyModelForm(ModelForm):
    template_name_p = 'boot_form.html'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            # print(field.widget.is_required)
            field.widget.attrs['class'] = 'form-control'


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": 'ユーザー名またはパスワードが違います。',
        "inactive": "このアカウントは無効です。",
    }

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
