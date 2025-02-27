from django import forms
from authors.utils.django_forms import add_placeholder  # type: ignore


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Username...')
        add_placeholder(self.fields['password'], 'Password...')

    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput()
    )
