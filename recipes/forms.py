from django import forms
from django.forms.models import inlineformset_factory
from .models import User, Recipe, Ingredient, RecipeIngredient

class RecipeCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(RecipeCreateForm, self).__init__(*args, **kwargs)
        self.fields['num_serving'].initial = 4
    class Meta:
        model = Recipe
        # exclude = ['author', 'date_posted']
        exclude = ['author', 'ingredients', 'date_posted']
        labels = {
            'name': 'Title',
            'num_serving': 'Serves'
        }

# class IngredientAddForm(forms.ModelForm):
#     class Meta:
#         model = Ingredient
#         fields = ['name']
#         labels = {
#             'name': 'Cannot find your ingredient in the list? Add it here'
#         }

class RecipeIngredientForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'unit', 'amount']
        labels = {
            'ingredient': 'Ingredient name'
        }
        widgets = {
            'ingredient': forms.TextInput(),
            'class': 'form-control'
        }

    # def clean_ingredient(self):
    #     ingredient = self.form.cleaned_data['ingredient']
    #     if ingredient not in Ingredient.objects.all():
    #         new_ingredient = Ingredient.objects.create(name=ingredient)
    #         new_ingredient.save()
    #     return self.cleaned_data

class RecipeIngredientUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingredient'].widget.attrs['disabled'] = True
    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'unit', 'amount']
        labels = {
            'ingredient': 'Ingredient name'
        }
        widgets = {
            'class': 'form-control'
        }


RecipeIngredientFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=5, can_delete=False)
RecipeIngredientUpdateFormSet = inlineformset_factory(Recipe, RecipeIngredient, form=RecipeIngredientUpdateForm, extra=0, can_delete=True)
# RecipeIngredientUpdateFormSet = inlineformset_factory(Recipe, Recipe.ingredients.through, form=RecipeIngredientUpdateForm, extra=0, can_delete=True)
