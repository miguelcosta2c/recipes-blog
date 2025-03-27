from django.views.generic import ListView, DetailView
from django.http import Http404
from django.db.models import Q

from recipes.models import Recipe  # type: ignore
from recipes.utils.make_pagination import make_pagination

import os

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    template_name = "CHANGE-ME"
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        return qs.filter(is_published=True)

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get("recipes", []),
            PER_PAGE
        )
        new_context = {
            "recipes": page_obj,
            "pagination_range": pagination_range
        }
        ctx.update(new_context)
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = "recipes/pages/home.html"


class RecipeListViewCategory(RecipeListViewBase):
    template_name = "recipes/pages/category.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(category__pk=self.kwargs.get("pk"))
        if not qs:
            raise Http404()
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        recipes = self.get_queryset()
        category_name = recipes[0].category.name
        ctx.update(
            {
                "recipes": recipes,
                'title': f'{category_name} - Category | Recipes'
            }
        )
        return ctx


class RecipeListViewSearch(RecipeListViewBase):
    template_name = "recipes/pages/search.html"

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self.search_term = self.request.GET.get('q', '').strip()
        if not self.search_term:
            raise Http404()

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=self.search_term) |
                Q(description__icontains=self.search_term)
            ),
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        new_context = {
            'title': f'"{self.search_term}" - Search | Recipes',
            'search_term': self.search_term,
            'additional_url_query': f'&q={self.search_term}'
        }
        ctx.update(new_context)
        return ctx


class RecipeDetailView(DetailView):
    model = Recipe
    context_object_name = "recipe"
    template_name = "recipes/pages/recipe.html"

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx.update({"is_detail_page": True})
        return ctx
