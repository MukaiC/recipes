# from django.conf import settings

from django.contrib import messages
# from django.forms import formset_factory
from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from .models import User, Recipe, Ingredient, RecipeIngredient
from .forms import RecipeCreateForm, IngredientAddForm, RecipeIngredientForm, RecipeIngredientFormSet



class RecipesListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-date_posted']

class RecipesDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe.html'
    context_object_name = 'recipe'

# class RecipeCreateView(CreateView):
#     model = Recipe
#     fields = ['name', 'description', 'method', 'header_image', 'num_serving', 'ingredients']


def create_recipe(request):
    if request.method == 'POST':
        recipe_form = RecipeCreateForm(request.POST)
        recipe_ing_formset = RecipeIngredientFormSet(request.POST, request.FILES)
        
        if recipe_form.is_valid() and recipe_ing_formset.is_valid():
            # Save the forms
            pass

    else:
        recipe_form = RecipeCreateForm()
        recipe_ing_formset = RecipeIngredientFormSet()

    context = {
        'recipe_form': recipe_form,
        'recipe_ing_formset': recipe_ing_formset
    }
    return render(request, 'recipes/create.html', context)

def search(request):
    results = []
    # Get the search input
    q = request.GET.get('q')
    # Get recipes
    recipes = Recipe.objects.all()
    for recipe in recipes:
        if q.lower() in recipe.name.lower():
            results.append(recipe)
    context = {
        'results': True,
        'search_for': q,
        'recipes': [recipe.serialize_simple() for recipe in results],
    }
    # messages.success(request, 'Your search result.')
    return render(request, 'recipes/home.html', context)

def about(request):
    return render(request, 'recipes/about.html', {'title': 'About'})

# from django.http import HttpResponse

# recipes = [
#     {'title': 'Boiled eggs', 'subtitle': 'Learn how to make boiled eggs.' ,'author': 'author 1', 'date_posted': 'Sept. 3 2020'},
#     {'title': 'Simple green salad', 'subtitle': 'Learn how to make simple green salad.' ,'author': 'author 1', 'date_posted': 'Sept. 3 2020'},
# ]

# def index(request):
#     # Query all recipes in a reverse chronological order
#     recipes = Recipe.objects.order_by('-date_posted')
#     context = {
#         # Serialize each recipe and put them in a list
#         'recipes': [recipe.serialize_simple() for recipe in recipes]
#     }
#     return render(request, 'recipes/home.html', context)


# def recipe(request, recipe_id):
#     recipe = Recipe.objects.get(id=recipe_id)
#     context = {
#         'recipe': recipe.serialize(),
#         'title': recipe.name
#     }
#     return render(request, 'recipes/recipe.html', context)

# def create_recipe(request):
#     recipe_form = RecipeCreateForm()
#     # ing_formset = formset_factory(IngredientAddForm)
#     # ing_formset = IngredientAddForm()
#     # recipe_ing_form = RecipeIngredientForm()
#     recipe_ing_formset = RecipeIngredientFormSet()
#     context = {
#         'recipe_form': recipe_form,
#         # 'ing_form': ing_formset,
#         # 'recipe_ing_form': recipe_ing_form
#         'recipe_ing_formset': recipe_ing_formset
#     }
#     return render(request, 'recipes/create.html', context)
