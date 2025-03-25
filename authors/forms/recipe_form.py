from django import forms
from recipes.models import Recipe  # type: ignore
from authors.utils.django_forms import generator_add_attr  # type: ignore

add_class = generator_add_attr("class")
def add_span(field): return add_class(field, 'span-2')


class AuthorRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        add_span(self.fields.get('title'))
        add_span(self.fields.get('description'))
        add_span(self.fields.get('preparation_steps'))

    title = forms.CharField(
        label="Title",
        strip=True,
        required=True,
        min_length=5,
        max_length=65,
        error_messages={
            "required": "Type a title.",
            "min_length": "Must have at least 5 characters.",
            "max_length": "Must have a maximum of 65 characters.",
        }
    )

    description = forms.CharField(
        label="Description",
        strip=True,
        required=True,
        min_length=10,
        max_length=165,
        error_messages={
            "required": "Type a description.",
            "min_length": "Must have at least 5 characters.",
            "max_length": "Must have a maximum of 65 characters.",
        }
    )

    preparation_time = forms.IntegerField(
        label="Preparation time",
        required=True,
        min_value=1,
        max_value=99,
        error_messages={
            "required": "Type a number.",
            "min_value": "The minimum value must be 1",
            "max_value": "The maximum value must be 99",
            "invalid": "An invalid value was entered."
        }
    )

    servings = forms.IntegerField(
        label="Servings",
        required=True,
        min_value=1,
        max_value=999,
        error_messages={
            "required": "Type a number.",
            "min_value": "The minimum value must be 1",
            "max_value": "The maximum value must be 999",
            "invalid": "An invalid value was entered."
        }
    )

    class Meta:
        model = Recipe
        fields = (
            'title',
            'description',
            'preparation_time',
            'preparation_time_unit',
            'preparation_steps',
            'servings',
            'servings_unit',
            'cover'
        )
        widgets = {
            "cover": forms.FileInput(
                attrs={
                    "class": "span-2"
                }
            ),
            "servings_unit": forms.Select(
                choices=(
                    ("Portions", "Portions"),
                    ("Pieces", "Pieces"),
                    ("People", "People"),
                )
            ),
            "preparation_time_unit": forms.Select(
                choices=(
                    ("Days", "Days"),
                    ("Minutes", "Minutes"),
                    ("Seconds", "Seconds"),
                    ("Hours", "Hours"),
                )
            )
        }

    def clean(self, *args, **kwargs):
        super_clean = super().clean(*args, **kwargs)
        cd = self.cleaned_data

        title = cd.get("title", "")
        description = cd.get("description", "")

        if title == description:
            self.add_error("title", "Title cannot be equal to description")

        return super_clean
