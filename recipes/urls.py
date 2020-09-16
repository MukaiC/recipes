from django.urls import path
from . import views
from users import views as users_views

app_name = 'recipes'
urlpatterns = [
    path('', views.index, name='index'),
    path('login', users_views.login_view, name='login'),
    path('about/', views.about, name='about'),
    path('recipe/<int:recipe_id>', views.recipe, name='recipe'),
    path('search', views.search, name='search'),

]
