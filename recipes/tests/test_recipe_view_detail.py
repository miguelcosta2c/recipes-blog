from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):
    def test_recipe_detail_views_function(self):
        view = resolve(reverse('recipes:recipe', kwargs={'pk': 1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_status_404(self):
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1000})
        )
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_shows_recipe(self):
        self.make_recipe()
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': 1}))
        recipe_context = response.context['recipe']
        response_content = response.content.decode()

        self.assertIn(recipe_context.title, response_content)

    def test_recipe_detail_is_published(self):
        recipe = self.make_recipe(is_published=False)
        response = self.client.get(
            reverse('recipes:recipe', kwargs={'pk': recipe.pk})
        )
        self.assertEqual(response.status_code, 404)
