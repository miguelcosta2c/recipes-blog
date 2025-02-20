from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django import http

from .forms import RegisterForm


def register_post_tratament(post):
    if post:
        post['first_name'] = post['first_name'].strip()
        post['last_name'] = post['last_name'].strip()
        post['username'] = post['username'].strip()
        post['email'] = post['email'].strip()
        post['password'] = post['password'].strip()
        post['password2'] = post['password2'].strip()


def register_view(request: http.HttpRequest) -> http.HttpResponse:
    register_form_data = request.session.get('register_form_data')
    register_post_tratament(register_form_data)
    form = RegisterForm(register_form_data)
    context = {
        'form': form,
        'title': ' - Authors | Recipes',
        'form_action': reverse('authors:create')
    }
    return render(request, 'authors/pages/register_view.html', context)


def register_create(request: http.HttpRequest):
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

    return redirect('authors:register')
