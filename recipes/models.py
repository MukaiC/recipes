from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from extra_views import UpdateWithInlinesView, InlineFormSetFactory
from PIL import Image

UNIT_CHOICES =  [
    ('NA', 'Select a unit'),
    ('tbs', 'tbs'),
    ('tsp', 'tsp'),
    ('cup', 'cup'),
    ('cups', 'cups'),
    ('g', 'g'),
    ('kg','kg'),
    ('ml', 'ml'),
    ('l', 'L')
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
    header_image = models.ImageField(null=True, blank=True, default='default_food.png', upload_to='images/')
    num_serving = models.IntegerField(null=True)
    ingredients = models.ManyToManyField('Ingredient', through='RecipeIngredient', related_name='recipes')
    date_posted = models.DateTimeField(default=timezone.now)


    # def serialize(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'description': self.description,
    #         'method': self.method,
    #         'author': self.author.username,
    #         'serves': self.num_serving,
    #         'month_posted':self.date_posted.strftime("%B %Y"),
    #         'ingredients': [ingredient.name for ingredient in self.ingredients.all()]
    #     }
    #
    # def serialize_simple(self):
    #     return {
    #         'id': self.id,
    #         'name': self.name,
    #         'description': self.description,
    #         'author': self.author.username,
    #         'date_posted':self.date_posted.strftime("%b %d %Y"),
    #     }

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('recipes:recipe', kwargs={'pk':self.pk})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.header_image:
            img = Image.open(self.header_image.path)
            # if the image size is bigger than 300px, shrink it to output_size
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.header_image.path)

class Ingredient(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

class RecipeIngredient(models.Model):
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE, related_name='recipeingredients')
    ingredient = models.ForeignKey('Ingredient', on_delete=models.CASCADE, related_name='recipeingredients')
    unit = models.CharField(max_length=30, blank=True, choices=UNIT_CHOICES)
    amount = models.CharField(max_length=30, null=True, blank=True)
    # amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.ingredient.name
        # return f"{self.ingredient} for {self.recipe} recipe"

    def get_absolute_url(self):
        return reverse('recipes:update', kwargs={'pk':self.recipe})
