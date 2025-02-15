from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404, HttpRequest, HttpResponse
from django.db.models import Q

from recipes.models import Recipe  # type: ignore
from recipes.utils.make_pagination import make_pagination

import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


def home(request: HttpRequest) -> HttpResponse:
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request,
        recipes,
        PER_PAGE
    )

    context = {
        'recipes': page_obj,
        'pagination_range': pagination_range
    }
    return render(request, 'recipes/pages/home.html', context)


def recipe(request: HttpRequest, pk: int) -> HttpResponse:
    recipe = get_object_or_404(
        Recipe.objects.filter(is_published=True, pk=pk)
    )
    context = {
        'recipe': recipe,
        'title': f'{recipe.title} - Recipe | Recipes',
        'is_detail_page': True
    }
    return render(request, 'recipes/pages/recipe.html', context)


def category(request: HttpRequest, pk: int) -> HttpResponse:
    recipes = get_list_or_404(
        Recipe.objects
        .filter(category__pk=pk, is_published=True)
        .order_by('-id')
    )
    category_name: str = recipes[0].category.name

    page_obj, pagination_range = make_pagination(
        request,
        recipes,
        PER_PAGE
    )

    context = {
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'title': f'{category_name} - Category | Recipes'
    }
    return render(request, 'recipes/pages/category.html', context)


def search(request: HttpRequest) -> HttpResponse:
    search_term = request.GET.get('q', '').strip()
    if not search_term:
        raise Http404()

    recipes = Recipe.objects.filter(
        Q(
            Q(title__icontains=search_term) |
            Q(description__icontains=search_term)
        ),
        is_published=True
    ).order_by('-id')

    page_obj, pagination_range = make_pagination(
        request,
        recipes,
        PER_PAGE
    )

    context = {
        'title': f'"{search_term}" - Search | Recipes',
        'search_term': search_term,
        'recipes': page_obj,
        'pagination_range': pagination_range,
        'additional_url_query': f'&q={search_term}'
    }
    return render(request, 'recipes/pages/search.html', context)
