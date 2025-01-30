from . import views
from django.urls import path

app_name = 'recipes'

urlpatterns = [
    path("", views.home, name="home"),
    path("recipes/<int:id>", views.recipe, name="recipe")
]
