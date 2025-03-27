from django.views.generic import ListView, DetailView
from django.http import Http404, JsonResponse
from django.forms.models import model_to_dict
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
        qs = qs.filter(is_published=True).select_related('author', 'category')
        return qs

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


class RecipeListViewHomeApi(RecipeListViewHome):
    def render_to_response(self, context, **kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = list(recipes.object_list.values())
        return JsonResponse(
            recipes_list,
            safe=False
        )


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


class RecipeDetailApi(RecipeDetailView):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)
        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)
        if recipe_dict.get('cover', ''):
            print(recipe_dict.get('cover', ''))
            recipe_dict['cover'] = \
                self.request.build_absolute_uri(
            ) + recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ""
        return JsonResponse(
            recipe_dict,
            safe=False
        )
