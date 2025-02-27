from django.urls import path
from authors import views

app_name = 'authors'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('register/create/', views.register_create, name='create'),
    path('login/', views.login_view, name='login'),
    path('login/authenticate/', views.login_create, name='authenticate'),
    path('logout/', views.logout_view, name='logout'),
]
