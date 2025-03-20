from django import http
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from authors.utils.decorators import no_login_required
from authors.utils.django_forms import register_post_tratament
from authors.forms import RegisterForm, LoginForm  # type: ignore


@no_login_required
def register_view(request: http.HttpRequest) -> http.HttpResponse:
    register_form_data = request.session.get('register_form_data')
    register_post_tratament(register_form_data)
    form = RegisterForm(register_form_data)
    context = {
        'form': form,
        'form_title': 'Register',
        'title': ' - Authors | Recipes',
        'form_action': reverse('authors:create')
    }
    return render(request, 'authors/pages/register_view.html', context)


@no_login_required
def register_create(request: http.HttpRequest):  # noqa: E501
    if request.method != 'POST':
        raise http.Http404()

    request.session['register_form_data'] = request.POST
    form = RegisterForm(request.POST)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(user.password)
        user.save()
        messages.success(request, 'User has been registered, please log in')

        del request.session["register_form_data"]
        return redirect('authors:login')

    return redirect('authors:register')


def login_view(request: http.HttpRequest) -> http.HttpResponse:
    form = LoginForm()
    context = {
        'form': form,
        'form_title': 'Login',
        'title': ' - Authors | Recipes',
        'form_action': reverse('authors:authenticate')
    }
    return render(request, 'authors/pages/login_view.html', context)


def login_create(request: http.HttpRequest):
    if request.method != 'POST':
        raise http.Http404()
    login_url = reverse('authors:login')
    form = LoginForm(request.POST)
    if form.is_valid():
        authenticated = authenticate(
            username=form.cleaned_data.get('username', ''),
            password=form.cleaned_data.get('password', ''),
        )
        if authenticated is not None:
            messages.success(request, 'You are logged in')
            login(request, authenticated)
        else:
            messages.error(request, 'User invalid Credentials')
    else:
        messages.error(request, 'Form invalid credentials')
    return redirect(login_url)


@login_required(login_url='authors:login', redirect_field_name='next')
def logout_view(request: http.HttpRequest):
    is_post = request.method != 'POST'
    is_valid_user = request.POST.get('username', '') != request.user.get_username()  # noqa: E501
    if is_post or is_valid_user:
        messages.error(request, 'Invalid logout request')
        return redirect('authors:login')
    messages.success(request, 'Logged out successfully')
    logout(request)
    return redirect('authors:login')
