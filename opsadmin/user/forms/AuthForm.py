from django.contrib.auth.forms import AuthenticationForm

from django import forms
from django.utils.translation import gettext_lazy as _

class UserLoginForm(AuthenticationForm):

    username = forms.CharField(label=_('Username'), max_length=100)
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput, max_length=100,
        strip=False)
