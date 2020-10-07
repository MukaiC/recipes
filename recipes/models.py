from django.conf import settings
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

UNIT_CHOICES =  [
    ('', 'Select a unit'),
    ('tbs', 'tbs'),
    ('tsp', 'tsp'),
    ('cup', 'cup'),
    ('g', 'g'),
    ('kg','kg'),
    ('ml', 'ml'),
    ('l', 'litre')
]

# Cannot be moved to users.models.py mid-project due to dependancy issues
class User(AbstractUser):

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200, blank=True)
    method = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    header_image = models.ImageField(null=True, blank=True, upload_to='images/')
    num_serving = models.IntegerField(null=True)
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient', related_name='recipes')
    date_posted = models.DateTimeField(default=timezone.now)


    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'method': self.method,
            'author': self.author.username,
            'serves': self.num_serving,
            'month_posted':self.date_posted.strftime("%B %Y"),
            'ingredients': [ingredient.name for ingredient in self.ingredients.all()]
        }

    def serialize_simple(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'author': self.author.username,
            'date_posted':self.date_posted.strftime("%b %d %Y"),
        }

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='recipeingredients')
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='recipeingredients')
    unit = models.CharField(max_length=30, blank=True, choices=UNIT_CHOICES)
    amount = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.ingredient} for {self.recipe} recipe"

# class Image(models.Model):
#     recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='image')
#     image = models.ImageField(upload_to='images', blank=True, )
#
#     def __str__(self):
#         return self.recipe
