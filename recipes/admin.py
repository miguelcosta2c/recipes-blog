from django.contrib import admin
from recipes import models

# Register your models here.


@admin.register(models.Category)  # type: ignore
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Recipe)  # type: ignore
class RecipeAdmin(admin.ModelAdmin):
    ...
