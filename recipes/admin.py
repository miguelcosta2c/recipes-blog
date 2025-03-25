from django.contrib import admin
from recipes import models

# Register your models here.


@admin.register(models.Category)  # type: ignore
class CategoryAdmin(admin.ModelAdmin):
    ...


@admin.register(models.Recipe)  # type: ignore
class RecipeAdmin(admin.ModelAdmin):
    ordering = ['-id']

    list_display = ['id', 'title', 'created_at', 'is_published', 'author']
    list_display_links = ['title', 'created_at']
    list_filter = [
        'category',
        'author',
        'is_published',
        'preparation_steps_is_html',
    ]
    list_per_page = 10
    list_editable = ['is_published']

    search_fields = ['id', 'title', 'description', 'slug', 'preparation_steps']

    prepopulated_fields = {"slug": ["title"]}
