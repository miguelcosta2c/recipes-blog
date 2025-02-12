from .test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class RecipeCategoryTest(RecipeTestBase):
    def setUp(self) -> None:
        self.category_name = 'Category Testing'
        self.category = self.make_category(
            name=self.category_name
        )
        return super().setUp()

    def test_recipe_category_model_string_repr(self):
        self.assertEqual(str(self.category), self.category_name)

    def test_category_model_field_name_max_length_65(self):
        self.category.name = 'A' * 70
        with self.assertRaises(ValidationError):
            self.category.full_clean()
