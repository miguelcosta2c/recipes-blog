from django.urls import reverse, resolve
from recipes import views
from .test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):
    def test_recipe_search_view_function(self):
        view = resolve(reverse('recipes:search'))
        self.assertIs(view.func, views.search)

    def test_recipe_search_view_loads_template(self):
        response = self.client.get(reverse('recipes:search')+'?q=teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')

    def test_recipe_search_raises_404_if_no_search(self):
        response = self.client.get(reverse('recipes:search'))
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_escaped(self):
        response = self.client.get(reverse('recipes:search')+'?q=Teste')
        self.assertTemplateUsed(response, 'recipes/pages/search.html')
        self.assertIn(
            '&quot;Teste&quot;',
            response.content.decode()
        )

    def test_recipe_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one',
            title=title1,
            author_data={'username': 'one'}
        )

        recipe2 = self.make_recipe(
            slug='two',
            title=title2,
            author_data={'username': 'two'}
        )

        urlsearch = reverse('recipes:search')
        response1 = self.client.get(f'{urlsearch}?q={title1}')
        response2 = self.client.get(f'{urlsearch}?q={title2}')
        responseboth = self.client.get(f'{urlsearch}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, responseboth.context['recipes'])
        self.assertIn(recipe2, responseboth.context['recipes'])

    def test_recipe_can_find_recipe_by_description(self):
        description1 = 'This is recipe one'
        description2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one',
            description=description1,
            author_data={'username': 'one'}
        )

        recipe2 = self.make_recipe(
            slug='two',
            description=description2,
            author_data={'username': 'two'}
        )

        urlsearch = reverse('recipes:search')
        response1 = self.client.get(f'{urlsearch}?q={description1}')
        response2 = self.client.get(f'{urlsearch}?q={description2}')
        responseboth = self.client.get(f'{urlsearch}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, responseboth.context['recipes'])
        self.assertIn(recipe2, responseboth.context['recipes'])
