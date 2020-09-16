from django.urls import path
from . import views


app_name = 'recipes'
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('recipe/<int:recipe_id>', views.recipe, name='recipe'),
    path('search', views.search, name='search'),

]
