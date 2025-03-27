from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):
    def test_recipe_category_views_function(self):
        view = resolve(reverse('recipes:category', kwargs={'pk': 1}))
        self.assertIs(view.func.view_class, views.RecipeListViewCategory)

    def test_recipe_category_view_returns_status_404(self):
        response = self.client.get(
            reverse('recipes:category', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_shows_recipes(self):
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:category', kwargs={'pk': 1})
        )
        recipe_context = response.context['recipes'][0]
        response_content = response.content.decode()

        self.assertIn(recipe_context.title, response_content)

    def test_recipe_category_is_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:category', kwargs={'pk': recipe.category.pk})
        )
        self.assertEqual(response.status_code, 404)
