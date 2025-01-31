from django.shortcuts import render, get_list_or_404, get_object_or_404
from .utils.make_recipes import make_recipe
from .models import Recipe, Category
# Create your views here.


def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    context = {
        'recipes': recipes
    }
    return render(request, 'recipes/pages/home.html', context)


def recipe(request, pk):
    recipe = get_object_or_404(
        Recipe.objects.filter(is_published=True, pk=pk)
    )
    context = {
        'recipe': recipe,
        'title': f'{recipe.title} - Recipe | Recipes',
        'is_detail_page': True
    }
    return render(request, 'recipes/pages/recipe.html', context)


def category(request, pk):
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
