from django.contrib.auth.decorators import user_passes_test


def no_login_required(
    function=None, home_url='recipes:home'
):
    actual_decorator = user_passes_test(
        lambda user: not user.is_authenticated,
        login_url=home_url,
        redirect_field_name=None
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
