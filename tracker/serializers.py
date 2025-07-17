
from rest_framework import serializers
from .models import UserProfile, FoodLog

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['weight_kg', 'diet_choice', 'target_calories', 'target_protein', 'target_fat', 'target_carbs']
        # Make the target fields read-only
        read_only_fields = ['target_calories', 'target_protein', 'target_fat', 'target_carbs']

class FoodLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodLog
        exclude = ['user']