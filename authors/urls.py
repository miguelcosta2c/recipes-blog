from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
    path(
        'register/',
        views.register_view,
        name='register'
    ),
    path(
        'register/create/',
        views.register_create,
        name='create'
    ),
    path(
        'login/',
        views.login_view,
        name='login'
    ),
    path(
        'login/authenticate/',
        views.login_create,
        name='authenticate'
    ),
    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),
    path(
        'dashboard/',
        views.dashboard_view, name='dashboard'
    ),
    path(
        'dashboard/recipe/delete/',
        views.dashboard_recipe_delete_view,
        name='dashboard_recipe_delete'
    ),
    path(
        'dashboard/recipe/create/',
        views.dashboard_recipe_create_view,
        name='dashboard_recipe_create'
    ),
    path(
        'dashboard/recipe/<int:pk>/edit/',
        views.dashboard_recipe_edit_view,
        name='dashboard_recipe_edit'
    ),


]
