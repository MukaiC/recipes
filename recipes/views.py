# from django.conf import settings

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import ModelFormMixin
from .models import User, Recipe, Ingredient, RecipeIngredient
from .forms import RecipeCreateForm, RecipeIngredientForm, RecipeIngredientFormSet



class RecipesListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-date_posted']

class RecipesDetailView(DetailView):
    model = Recipe
    template_name = 'recipes/recipe.html'
    context_object_name = 'recipe'

class RecipeCreateView(LoginRequiredMixin, CreateView):
    model = Recipe
    template_name = 'recipes/create.html'
    form_class = RecipeCreateForm

    # Populate the context with the forms
    def get_context_data(self, **kwargs):
        context = super(RecipeCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            # context['recipe_form'] = RecipeCreateForm(self.request.POST)
            context['recipe_ing_formset'] = RecipeIngredientFormSet(self.request.POST, self.request.FILES)
        else:
            # context['recipe_form'] = RecipeCreateForm()
            context['recipe_ing_formset'] = RecipeIngredientFormSet()
        return context

    def form_valid(self, form):
        # new recipe object

        # for form in formset:
        #     ing = form['ingredient'].value()
        #     if ing not in ingredients:
        #         Ingredient.objects.create(name=ing)


        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        ingredients = [ing.name for ing in Ingredient.objects.all()]
        context = self.get_context_data()
        formset = context['recipe_ing_formset']

        # instances = formset.save(commit=False)
        for form in formset:
            ing = form['ingredient'].value().lower()
            if len(ing) > 0:
                if ing not in ingredients:
                    Ingredient.objects.create(name=ing)
                r_i = RecipeIngredient()
                r_i.recipe = self.object
                r_i.ingredient = Ingredient.objects.get(name=ing)
                r_i.unit = form['unit'].value()
                # r_i.amount = form['amount'].value()
                r_i.amount = form['amount'].value()

                # amount = form['amount'].value()
                # if amount == '':
                #     r_i.amount = '0.00'
                # else:
                #     r_i.amount = float(amount)

                    # r_i.amount = float(form['amount'].value())
                r_i.save()

        try:
            return super(ModelFormMixin, self).form_valid(form)
            # return super(self).form_valid(form)
        except:
            return render(self.request, 'recipes/create.html', self.get_context_data())
        # context = self.get_context_data()
        # # recipe_form = context['recipe_form']
        # formset = context['recipe_ing_formset']
        #
        # for form in formset:
        #     ing = form['ingredient']
        #     if ing not in ingredients:
        #         new_ing = Ingredient(name=ing)
        #         # new_ing.save()




# def create_recipe(request):
#     """Function based view to create a new recipe"""
#     if request.method == 'POST':
#         recipe_form = RecipeCreateForm(request.POST)
#         recipe_ing_formset = RecipeIngredientFormSet(request.POST, request.FILES)
#
#         if recipe_form.is_valid() and recipe_ing_formset.is_valid():
#             # Save the forms
#             pass
#
#     else:
#         recipe_form = RecipeCreateForm()
#         recipe_ing_formset = RecipeIngredientFormSet()
#
#     context = {
#         'recipe_form': recipe_form,
#         'recipe_ing_formset': recipe_ing_formset
#     }
#     return render(request, 'recipes/create.html', context)

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
