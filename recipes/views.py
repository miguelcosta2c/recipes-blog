from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import Http404, HttpRequest
from django.db.models import Q
from .models import Recipe  # type: ignore


def home(request: HttpRequest):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/pages/home.html', context)


def recipe(request: HttpRequest, pk: int):
    recipe = get_object_or_404(
        Recipe.objects.filter(is_published=True, pk=pk)
    )
    context = {
        'recipe': recipe,
        'title': f'{recipe.title} - Recipe | Recipes',
        'is_detail_page': True
    }
    return render(request, 'recipes/pages/recipe.html', context)


def category(request: HttpRequest, pk: int):
    recipes = get_list_or_404(
        Recipe.objects
        .filter(category__pk=pk, is_published=True)
        .order_by('-id')
    )
    category_name = recipes[0].category.name
    context = {
        'recipes': recipes,
        'title': f'{category_name} - Category | Recipes'
    }
    return render(request, 'recipes/pages/category.html', context)


def search(request: HttpRequest):
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

    context = {
        'title': f'"{search_term}" - Search | Recipes',
        'search_term': search_term,
        'recipes': recipes
    }
    return render(request, 'recipes/pages/search.html', context)
