# from django.conf import settings

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import ModelFormMixin
from .models import User, Recipe, Ingredient, RecipeIngredient
from .forms import RecipeCreateForm, RecipeIngredientForm, RecipeIngredientFormSet, RecipeIngredientUpdateFormSet



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
            context['recipe_ing_formset'] = RecipeIngredientFormSet(self.request.POST, self.request.FILES)
        else:
            context['recipe_ing_formset'] = RecipeIngredientFormSet()
        return context

    def form_valid(self, form):
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
                r_i.amount = form['amount'].value()
                r_i.save()

        try:
            return super(ModelFormMixin, self).form_valid(form)
            # return super(self).form_valid(form)
        except:
            return render(self.request, 'recipes/create.html', self.get_context_data())


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Recipe
    template_name = 'recipes/create.html'
    form_class = RecipeCreateForm

    def get_context_data(self, **kwargs):
        context = super(RecipeUpdateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['recipe_ing_formset'] = RecipeIngredientFormSet(self.request.POST, self.request.FILES)
            # context['recipe_ing_updateformset'] = RecipeIngredientFormSet( self.request.POST, self.request.FILES, instance=self.object)
            context['recipe_ing_updateformset'] = RecipeIngredientUpdateFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            context['recipe_ing_formset'] = RecipeIngredientFormSet()
            # context['recipe_ing_updateformset'] = RecipeIngredientFormSet(instance=self.object)
            context['recipe_ing_updateformset'] = RecipeIngredientUpdateFormSet(instance=self.object)


            # for form in context['recipe_ing_formset']:
            #     form['ingredient'].initial = self.object.recipeingredients.ingredient.name

            # context['recipe_ing_formset'] = RecipeIngredientFormSet(queryset = self.object.recipeingredients.all(), instance = self.object)
            # initial = [{'ingredient': obj.ingredient} for obj in self.object.recipeingredients.all()]
            # context['recipe_ing_formset'] = RecipeIngredientFormSet(queryset = RecipeIngredient.objects.filter(recipe=self.get_object()))
            # context['recipe_ing_formset'] = RecipeIngredientFormSet(queryset = self.get_object().recipeingredients.all())
        return context

    def form_valid(self, form):

        context = self.get_context_data()
        updateformset = context['recipe_ing_updateformset']
        formset = context['recipe_ing_formset']

        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        if updateformset.is_valid():
            updateformset.save()
            # for form in updateformset:
            #     ing = form['ingredient']
            #     r_i = RecipeIngredient()
            #     r_i.recipe = self.object
            #     r_i.ingredient = ing.field['ingredient']
            #     r_i.unit = form['unit'].value()
            #     r_i.amount = form['amount'].value()
            #     r_i.save()

            # updateformset.save()
            # updateformset = updateformset.save(commit=False)
            # for obj in updateformset:
            #     obj.save()

            # if updateformset.deleted_objects:
            #     for obj in updateformset.deleted_objects:
            #         obj.delete()

        else:
            return render(self.request, 'recipes/create.html', self.get_context_data())


        ingredients = [ing.name for ing in Ingredient.objects.all()]

        for form in formset:
            ing = form['ingredient'].value().lower()
            if len(ing) > 0:
                if ing not in ingredients:
                    Ingredient.objects.create(name=ing)
                r_i = RecipeIngredient()
                r_i.recipe = self.object
                r_i.ingredient = Ingredient.objects.get(name=ing)
                r_i.unit = form['unit'].value()
                r_i.amount = form['amount'].value()
                r_i.save()

        try:
            return super(ModelFormMixin, self).form_valid(form)
            # return super(self).form_valid(form)
        except:
            return render(self.request, 'recipes/create.html', self.get_context_data())


    # def get_initial(self):
    #     recipe_obj = self.get_object()
    #     values = recipe_obj.recipeingredients.values()
    #     initial = super(RecipeUpdateView, self).get_initial()
    #     # initial = super(self).get_initial()
    #     for i in values:
    #         # ingredient_obj = Ingredient.objects.get(id=i["ingredient_id"])
    #         # initial['ingredient'] = ingredient_obj.name
    #         initial['ingredient'] = Ingredient.objects.get(pk=ingredient_id)
    # #     # recipe_ing= self.get_object().recipeingredients.all()
    # #     recipe_ing_obj = RecipeIngredient.objects.filter(recipe=self.get_object())
    # #     for obj in recipe_ing_obj:
    # #         initial['ingredient'] = obj.ingredient.name
    # #         initial['unit'] = obj.unit
    # #         initial['amount'] = obj.amount
    # #     # for i in recipe_ing:
    # #     #     # initial['ingredient'] =
    # #     #     pass
    #     return initial

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        else:
            return False

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
