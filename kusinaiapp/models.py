from django.db import models
from django.contrib.auth.models import User

# Provided from signup and survey
class AppUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's User model
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=128)  # Ideally use Django's built-in password management
    family_size = models.IntegerField()
    age_range = models.JSONField()  # Assuming multiple data per user
    meal_preference = models.JSONField()  # Assuming multiple data per user
    allergies = models.JSONField()  # Assuming multiple data per user
    cooking_skills = models.CharField(max_length=200)  # Adjust field type as needed

    def __str__(self):
        return self.username


# Provided by admin
class Dish(models.Model):
    dish_name = models.CharField(max_length=200)
    preparation_time = models.DurationField()
    ingredient_list = models.JSONField()  # Assuming multiple data
    number_of_servings = models.IntegerField()
    procedure = models.TextField()
    nutritional_guide = models.TextField()
    skills_needed = models.CharField(max_length=200)
    age_range_that_can_eat = models.JSONField()  # Assuming multiple data
    cost = models.DecimalField(max_digits=6, decimal_places=2)
    dish_image = models.ImageField(upload_to='dish_images/')

    def __str__(self):
        return self.dish_name


# Provided from cooked page
class UserInteraction(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    rating = models.IntegerField()  # Assuming rating is an integer, adjust as needed

    class Meta:
        unique_together = ('user', 'dish')  # Ensure each user can only rate a dish once


# Provided from saving dish from home to saved page
class DishPlan(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    plan = models.CharField(max_length=100)  # Adjust field type as needed

    class Meta:
        unique_together = ('user', 'dish')  # Ensure unique plans per user and dish
