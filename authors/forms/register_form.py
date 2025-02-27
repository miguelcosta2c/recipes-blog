from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from authors.utils.django_forms import (add_placeholder, strong_password)


class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Username...')
        add_placeholder(self.fields['email'], 'E-mail...')
        add_placeholder(self.fields['first_name'], 'Ex: John...')
        add_placeholder(self.fields['last_name'], 'Ex: Doe...')
        add_placeholder(self.fields['password'], 'Password...')
        add_placeholder(self.fields['password2'], 'Repeat your password...')

    username = forms.CharField(
        label='Username',
        help_text=('Ex: johndoe'),
        required=True,
        min_length=4,
        max_length=150,
        error_messages={
            'required': ('Username cannot be empty'),
            'min_length': ('Username must be at least 4 characters long'),
            'max_length': ('Username must be at most 150 characters long'),
        },
    )

    first_name = forms.CharField(
        required=True,
        label='First name',
        error_messages={'required': ('First name cannot be empty')},
    )

    last_name = forms.CharField(
        required=True,
        label='Last name',
        error_messages={'required': ('Last name cannot be empty')},
    )

    email = forms.EmailField(
        required=True,
        label='E-mail',
        help_text=('Ex: johndoe@email.com'),
        error_messages={'required': ('E-mail cannot be empty')},
    )

    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Password',
        error_messages={
            'required': ('Password cannot be empty'),
            'min_length': ('Password must be at least 8 characters long'),
            'max_length': ('Password must be at most 150 characters long'),
        },
        validators=[strong_password],
        min_length=8,
        max_length=150,
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label='Repeat Password',
        error_messages={
            'required': ('Please repeat your password')
        },
    )

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email', '')
        exists = User.objects.filter(email=email).exists()

        if exists:
            self.add_error(
                'email',
                ValidationError(
                    ('Email is already in use'),
                    code='invalid'
                )
            )

        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")  # type: ignore
        password2 = cleaned_data.get("password2")  # type: ignore

        if password and password2 and password != password2:
            self.add_error(
                None,
                ValidationError(
                    ('Passwords must be the same'),
                    code='invalid'
                )
            )

        return cleaned_data
