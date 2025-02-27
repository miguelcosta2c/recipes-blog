from django.core.exceptions import ValidationError

import re


def generator_add_attr(attr):
    def _inner(field, value):
        field.widget.attrs[attr] = value.strip()
    return _inner


add_placeholder = generator_add_attr('placeholder')


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])\S*$')

    if not regex.match(password):
        raise ValidationError(
            (
                'Password must have at least one uppercase, '
                'Password must contain at least one uppercase letter, '
                'one lowercase letter, '
                'and one number, with no spaces.'
            ),
            code='invalid'
        )


def register_post_tratament(post):
    fields = ['first_name', 'last_name', 'username', 'email', 'password',
              'password2']
    if not post:
        return
    for field in fields:
        post[field] = post[field].strip()
