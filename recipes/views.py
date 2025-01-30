from django.shortcuts import render
from .utils.make_recipes import make_recipe
# Create your views here.


def home(request):
    context = {
        'recipes': [make_recipe(c) for c in range(1, 21, 2)]
    }
    return render(request, 'recipes/pages/home.html', context)


def recipe(request, id):
    context = {
        'recipe': make_recipe(),
        'is_detail_page': True
    }
    return render(request, 'recipes/pages/recipe.html', context)
