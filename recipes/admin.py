from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Recipe, Ingredient, RecipeIngredient

class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'date_posted')

class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient')

admin.site.register(User, UserAdmin)
admin.site.register(Recipe, RecipeAdmin)
# admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
