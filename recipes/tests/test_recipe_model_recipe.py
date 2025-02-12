from .test_recipe_base import RecipeTestBase
from ..models import Recipe  # type: ignore
from django.core.exceptions import ValidationError
from parameterized import parameterized  # type: ignore


class RecipeModelTest(RecipeTestBase):
    def setUp(self) -> None:
        self.recipe = self.make_recipe()
        return super().setUp()

    def make_recipe_nodefaults(self):
        recipe = Recipe(
            category=self.make_category(name='Test Default Category'),
            author=self.make_author(username='newuser'),
            title='Recipe Title',
            description='Recipe Decription',
            slug='recipe-slug',
            preparation_time='10',
            preparation_time_unit='Minutes',
            servings='5',
            servings_unit='Servings',
            preparation_steps='Recipe Preparation Step',
        )
        recipe.full_clean()
        recipe.save()
        return recipe

    def test_recipe_raises_error_max_length(self):
        self.recipe.title = 'A' * 70  # more than 64
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    @parameterized.expand([
        ('title', 65),
        ('description', 165),
        ('preparation_time_unit', 165),
        ('servings_unit', 65),
    ])
    def test_recipe_fields_max_length_65(self, field, max_length):
        setattr(self.recipe, field, 'A' * (max_length + 1))
        with self.assertRaises(ValidationError):
            self.recipe.full_clean()

    def test_recipe_preparation_steps_is_html_default_value_is_false(self):
        recipe = self.make_recipe_nodefaults()
        self.assertFalse(recipe.preparation_steps_is_html,
                         msg='Recipe.preparation_steps_is_html is not False')

    def test_recipe_is_published_default_value_is_false(self):
        recipe = self.make_recipe_nodefaults()
        self.assertFalse(recipe.is_published,
                         msg='Recipe.is_published is not False')

    def test_recipe_string_repr(self):
        title = 'Testing Repr'
        self.recipe.title = title
        self.recipe.full_clean()
        self.recipe.save()
        self.assertEqual(
            str(self.recipe), title,
            msg=f'Recipe String Repr must be recipe title: {title}'
        )
