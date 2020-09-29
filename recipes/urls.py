from django.urls import path
from .views import RecipesListView, RecipesDetailView
from . import views


app_name = 'recipes'
urlpatterns = [
    # path('', views.index, name='index'),
    # path('recipe/<int:recipe_id>', views.recipe, name='recipe'),
    path('', RecipesListView.as_view(), name='index'),
    path('recipe/<int:pk>', RecipesDetailView.as_view(), name='recipe'),
    path('about/', views.about, name='about'),
    path('search', views.search, name='search'),

]
