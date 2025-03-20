from django.test import TestCase
from django.contrib.auth.models import User
from recipes import models


class RecipeMixin:
    def make_category(self, name="Category"):
        return models.Category.objects.create(name=name)

    def make_author(
        self,
        username="testuser1username",
        email="testuser@email.com",
        password="testing123",
        first_name="TestUserName",
        last_name="Test User Lastname",
    ):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

    def make_recipe(
        self,
        category_data=None,
        author_data=None,
        title='Recipe Title',
        description='Recipe Decription',
        slug='recipe-slug',
        preparation_time='10',
        preparation_time_unit='Minutes',
        servings='5',
        servings_unit='Servings',
        preparation_steps='Recipe Preparation Step',
        preparation_steps_is_html=False,
        is_published=True
    ):
        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}

        return models.Recipe.objects.create(
            category=self.make_category(**category_data),
            author=self.make_author(**author_data),
            title=title,
            description=description,
            slug=slug,
            preparation_time=preparation_time,
            preparation_time_unit=preparation_time_unit,
            servings=servings,
            servings_unit=servings_unit,
            preparation_steps=preparation_steps,
            preparation_steps_is_html=preparation_steps_is_html,
            is_published=is_published
        )

    def make_recipes_in_batch(self, qtd=10):
        recipes = []
        for i in range(1, qtd+1):
            kwargs = {
                'author_data': {'username': f'Author{i}'},
                'title': f'Title {i}',
                'slug': f'slug-{i}',
            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes


class RecipeTestBase(TestCase, RecipeMixin):
    ...
