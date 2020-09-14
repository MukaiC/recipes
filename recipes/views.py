from django.shortcuts import render
from .models import User, Recipe, Ingredient, RecipeIngredient


# from django.http import HttpResponse

# recipes = [
#     {'title': 'Boiled eggs', 'subtitle': 'Learn how to make boiled eggs.' ,'author': 'author 1', 'date_posted': 'Sept. 3 2020'},
#     {'title': 'Simple green salad', 'subtitle': 'Learn how to make simple green salad.' ,'author': 'author 1', 'date_posted': 'Sept. 3 2020'},
# ]

def index(request):
    # Query all recipes in a reverse chronological order
    recipes = Recipe.objects.order_by('-date_posted')
    context = {
        # Serialize each recipe and put them in a list
        'recipes': [recipe.serialize_simple() for recipe in recipes]
    }
    return render(request, 'recipes/home.html', context)


def about(request):
    return render(request, 'recipes/about.html', {'title': 'About'})

def recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    context = {
        'recipe': recipe.serialize(),
        'title': recipe.name
    }
    return render(request, 'recipes/recipe.html', context)

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
        'message': 'results',
        'search_for': q,
        'recipes': [recipe.serialize_simple() for recipe in results]
    }
    return render(request, 'recipes/home.html', context)
