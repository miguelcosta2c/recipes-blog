from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeViewsTest(RecipeTestBase):
    def test_recipe_home_views_function(self):
        view = resolve(reverse('recipes:home'))
        self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_status_200(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertEqual(response.status_code, 200)

    def test_recipe_home_view_loads_template(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertTemplateUsed(response, 'recipes/pages/home.html')

    def test_recipe_home_shows_not_found_recipes(self):
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_home_shows_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipes:home'))
        recipe_context = response.context['recipes'].first()
        response_content = response.content.decode()

        self.assertIn(recipe_context.title, response_content)

    def test_recipe_home_is_published(self):
        self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipes:home'))
        self.assertIn(
            'No recipes found',
            response.content.decode('utf-8')
        )

    def test_recipe_category_views_function(self):
        view = resolve(reverse('recipes:category', kwargs={'pk': 1}))
        self.assertIs(view.func, views.category)

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
