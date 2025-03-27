from . import views
from django.urls import path

app_name = 'recipes'

urlpatterns = [
    path("",
         views.RecipeListViewHome.as_view(), name="home"),
    path('recipes/search/',
         views.RecipeListViewSearch.as_view(), name="search"),
    path("recipes/category/<int:pk>/",
         views.RecipeListViewCategory.as_view(), name="category"),
    path("recipes/<int:pk>/",
         views.RecipeDetailView.as_view(), name="recipe"),
    path("recipes/api/v1/",
         views.RecipeListViewHomeApi.as_view(), name="recipes_api_v1"),
    path("recipes/api/v1/<int:pk>/",
         views.RecipeDetailApi.as_view(), name="recipes_api_v1_detail"),
]
