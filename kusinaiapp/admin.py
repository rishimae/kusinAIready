from django.contrib import admin
from .models import AppUser, Dish, UserInteraction, DishPlan

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'name', 'phone_number', 'family_size', 'cooking_skills', 'formatted_age_range', 'formatted_meal_preference', 'formatted_allergies')
    search_fields = ('username', 'name', 'phone_number')
    
    def formatted_age_range(self, obj):
        return ', '.join(obj.age_range) if obj.age_range else 'N/A'
    formatted_age_range.short_description = 'Age Range'

    def formatted_meal_preference(self, obj):
        return ', '.join(obj.meal_preference) if obj.meal_preference else 'N/A'
    formatted_meal_preference.short_description = 'Meal Preference'

    def formatted_allergies(self, obj):
        return ', '.join(obj.allergies) if obj.allergies else 'N/A'
    formatted_allergies.short_description = 'Allergies'

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ('id', 'dish_name', 'preparation_time', 'number_of_servings', 'cost')
    search_fields = ('dish_name', 'ingredient_list', 'skills_needed')
    list_filter = ('skills_needed', 'cost')

@admin.register(UserInteraction)
class UserInteractionAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish', 'rating')
    search_fields = ('user__username', 'dish__dish_name')

@admin.register(DishPlan)
class DishPlanAdmin(admin.ModelAdmin):
    list_display = ('user', 'dish', 'plan')
    search_fields = ('user__username', 'dish__dish_name', 'plan')
