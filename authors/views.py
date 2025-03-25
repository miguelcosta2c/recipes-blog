from django import http
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify

from authors.utils.decorators import no_login_required
from authors.utils.django_forms import register_post_tratament
from authors.forms import (  # type: ignore
    AuthorRecipeForm,
    LoginForm,
    RegisterForm
)

from recipes.models import Recipe  # type: ignore
from recipes.views import PER_PAGE  # type: ignore
from recipes.utils.make_pagination import make_pagination


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
    dashboard_url = reverse('authors:dashboard')
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
    return redirect(dashboard_url)


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


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_view(request: http.HttpRequest):
    recipes = Recipe.objects.filter(
        is_published=False,
        author=request.user
    )

    page_obj, pagination_range = make_pagination(
        request,
        recipes,
        PER_PAGE
    )

    context = {
        "recipes": page_obj,
        "pagination_range": pagination_range
    }
    return render(
        request,
        'authors/pages/dashboard.html',
        context
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_edit_view(request: http.HttpRequest, pk: int):
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=pk
    ).first()

    if not recipe:
        raise http.Http404()

    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None,
        instance=recipe
    )

    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.slug = slugify(recipe.title)

        recipe.save()

        messages.success(request, 'Your recipe has been saved successfully!')
        return redirect(reverse('authors:dashboard_recipe_edit', args=(pk,)))

    context = {
        "form": form,
        "recipe": recipe
    }
    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_create_view(request: http.HttpRequest):
    form = AuthorRecipeForm(
        data=request.POST or None,
        files=request.FILES or None
    )
    if form.is_valid():
        recipe = form.save(commit=False)

        recipe.author = request.user
        recipe.preparation_steps_is_html = False
        recipe.is_published = False
        recipe.slug = slugify(recipe.title)

        recipe.save()

        messages.success(request, 'Your recipe has been created successfully!')
        return redirect(reverse('authors:dashboard_recipe_edit',
                                args=(recipe.id,)))

    context = {
        "form": form,
    }

    return render(
        request,
        'authors/pages/dashboard_recipe.html',
        context
    )


@login_required(login_url='authors:login', redirect_field_name='next')
def dashboard_recipe_delete_view(request: http.HttpRequest):
    if request.method != "POST":
        raise http.Http404()

    pk = request.POST.get("id")
    recipe = Recipe.objects.filter(
        is_published=False,
        author=request.user,
        pk=pk
    ).first()

    if not recipe:
        raise http.Http404()

    recipe.delete()
    messages.success(request, f"{recipe.title} has been deleted successfully")
    return redirect(reverse("authors:dashboard"))
