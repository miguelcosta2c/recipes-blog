from django import http
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from recipes.models import Recipe  # type: ignore

from authors.forms import AuthorRecipeForm  # type: ignore


@method_decorator(
    login_required(
        login_url="authors:login",
        redirect_field_name="next"
    ),
    name='dispatch'
)
class DashboardRecipe(View):
    def get_recipe(self, pk):
        if not pk:
            return None
        recipe = Recipe.objects.filter(
            is_published=False,
            author=self.request.user,
            pk=pk
        ).first()

        if not recipe:
            raise http.Http404()

        return recipe

    def get(self, *args, **kwargs):
        recipe = self.get_recipe(kwargs.get('pk'))
        form = AuthorRecipeForm(instance=recipe)
        return self.render_recipe(form, recipe)

    def post(self, *args, **kwargs):
        pk = kwargs.get('pk')
        recipe = self.get_recipe(pk)
        form = AuthorRecipeForm(
            data=self.request.POST or None,
            files=self.request.FILES or None,
            instance=recipe
        )
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = self.request.user
            recipe.preparation_steps_is_html = False
            recipe.is_published = False
            recipe.slug = slugify(recipe.title)
            recipe.save()
            messages.success(
                self.request, 'Your recipe has been saved successfully!'
            )
            return redirect(
                reverse('authors:dashboard_recipe_edit', args=(recipe.id,))
            )

        return self.render_recipe(form)

    def render_recipe(self, form, recipe=None):
        context = {"form": form}
        if recipe is not None:
            context["recipe"] = recipe
        return render(
            self.request,
            'authors/pages/dashboard_recipe.html',
            context
        )


@method_decorator(
    login_required(
        login_url="authors:login",
        redirect_field_name="next"
    ),
    name='dispatch'
)
class DashboardRecipeDelete(DashboardRecipe):
    def get(self, *args, **kwargs):
        raise http.Http404()

    def post(self, *args, **kwargs):
        pk = self.request.POST.get('id')
        recipe = self.get_recipe(pk)
        if recipe is not None:
            recipe.delete()
            messages.success(
                self.request, f"{recipe.title} has been deleted successfully"
            )
        else:
            messages.error(self.request, "An error occurred. Try again")
        return redirect(reverse("authors:dashboard"))
