# from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
# from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.views.generic.edit import ModelFormMixin
from .models import User, Recipe, Ingredient, RecipeIngredient
from .forms import RecipeCreateForm, RecipeIngredientForm,  RecipeIngredientFormSet, RecipeIngredientUpdateForm
# RecipeIngredientUpdateFormSet
from extra_views import UpdateWithInlinesView, InlineFormSetFactory, CreateWithInlinesView



class RecipesListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'
    ordering = ['-date_posted']

class AuthorListView(ListView):
    model = Recipe
    template_name = 'recipes/home.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(author=self.kwargs['pk']).order_by('-date_posted')

    def get_context_data(self, **kwargs):
        # Add the author in the context to use in the template
        context = super().get_context_data(**kwargs)
        context['author'] = get_object_or_404(User, id=self.kwargs['pk'])
        return context

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

        except:
            return render(self.request, 'recipes/create.html', self.get_context_data())




class RecipeIngredientInline(InlineFormSetFactory):
    model = RecipeIngredient
    # fields = ['ingredient', 'unit', 'amount']
    form_class = RecipeIngredientUpdateForm
    factory_kwargs = {'extra': 0}

class AddIngredientInline(InlineFormSetFactory):
    model = RecipeIngredient
    fields = ['ingredient', 'unit', 'amount']
    # form_class = RecipeIngredientForm
    factory_kwargs = {'extra': 5, 'can_delete':False}


def add_ingredients(request, pk):
    if request.method == "POST":
        formset = RecipeIngredientFormSet(request.POST)
        recipe_obj = Recipe.objects.get(pk=pk)

        ingredients = [ing.name for ing in Ingredient.objects.all()]
        for form in formset:
            ing = form['ingredient'].value().lower()
            if len(ing) > 0:
                if ing not in ingredients:
                    Ingredient.objects.create(name=ing)
                r_i = RecipeIngredient()
                r_i.recipe = recipe_obj
                r_i.ingredient = Ingredient.objects.get(name=ing)
                r_i.unit = form['unit'].value()
                r_i.amount = form['amount'].value()
                r_i.save()

            return redirect('recipes:update', pk=recipe_obj.pk)

    else:
        formset = RecipeIngredientFormSet()

    return render(request,'recipes/ingredients.html', {'formset': formset})



class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateWithInlinesView):
    model = Recipe
    inlines = [RecipeIngredientInline]
    fields = ['name', 'description', 'method', 'header_image', 'num_serving']
    template_name = 'recipes/update.html'
    def get_success_url(self):
        return self.object.get_absolute_url()

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        else:
            return False


class RecipeDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Recipe
    success_url = '/'

    def test_func(self):
        recipe = self.get_object()
        if self.request.user == recipe.author:
            return True
        else:
            return False

def search(request):
    results = []
    # Get the search input
    q = request.GET.get('q')
    keywords = q.split()
    for keyword in keywords:
        recipes = Recipe.objects.filter(name__icontains=keyword)
        list_recipes = list(recipes)
        # Append recipe to results if it does not already contain the same recipe
        [results.append(recipe) for recipe in list_recipes if recipe not in results]

        # Get ingredients that contain the keyword
        ingredients = list(Ingredient.objects.filter(name__icontains=keyword))

        # Get recipes that include these ingredients
        for ing in ingredients:
            ing_recipes = list(ing.recipes.all())
            # Append the recipes to results if not already in the results
            [results.append(recipe) for recipe in ing_recipes if recipe not in results]

    context = {
        'results': True,
        'search_for': q,
        'recipes': results,
        # 'recipes': [recipe.serialize_simple() for recipe in results],
    }
    # messages.success(request, 'Your search result.')
    return render(request, 'recipes/home.html', context)


def about(request):
    return render(request, 'recipes/about.html', {'title': 'About'})
