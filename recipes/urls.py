from django.urls import path
from .views import RecipesListView, RecipesDetailView
# RecipeCreateView
from . import views


app_name = 'recipes'
urlpatterns = [
    # path('', views.index, name='index'),
    # path('recipe/<int:recipe_id>', views.recipe, name='recipe'),
    path('', RecipesListView.as_view(), name='index'),
    path('recipe/<int:pk>/', RecipesDetailView.as_view(), name='recipe'),
    # path('recipe/new/', RecipeCreateView.as_view(), name='create'),
    path('recipe/new/', views.create_recipe, name='create'),
    path('about/', views.about, name='about'),
    path('search/', views.search, name='search'),

]
