from . import views
from django.urls import path

app_name = 'recipes'

urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/category/<int:pk>", views.category, name="category"),
    path("recipes/<int:pk>", views.recipe, name="recipe"),
]
