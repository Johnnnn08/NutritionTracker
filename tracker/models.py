from django.db import models

# Create your models here.


from django.contrib.auth.models import User

class UserProfile(models.Model):
    DIET_CHOICES = [
        ('normal', 'Normal'),
        ('lose_fat', 'Lose Fat'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    weight_kg = models.FloatField(null=True, blank=True)
    diet_choice = models.CharField(max_length=10, choices=DIET_CHOICES, default='normal')
    
    
    target_calories = models.PositiveIntegerField(default=2000)
    target_protein = models.PositiveIntegerField(default=132)
    target_fat = models.PositiveIntegerField(default=70)
    target_carbs = models.PositiveIntegerField(default=250)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    def calculate_goals(self):
        # Cannot calculate without weight
        if not self.weight_kg:
            return 
    
       
        bmr = 22 * self.weight_kg
        tdee = bmr * 1.2

        # Adjust calories based on diet choice
        if self.diet_choice == 'lose_fat':
            self.target_calories = tdee - 500 # Create a 500 calorie deficit
            # source: https://www.mayoclinic.org/healthy-lifestyle/weight-loss/in-depth/calories/art-20048065
            # Macronutrient split for fat loss: 40% protein, 30% fat, 30% carbs
            # source: https://www.mdpi.com/2072-6643/9/8/822

            # Protein and carbs have 4 calories per gram, and fat has 9 calories per gram.
            self.target_protein = (self.target_calories * 0.40) / 4
            self.target_fat = (self.target_calories * 0.30) / 9
            self.target_carbs = (self.target_calories * 0.30) / 4
        else: # 'normal' diet
            self.target_calories = tdee # Maintain current weight
            # Balanced macronutrient split: 30% protein, 30% fat, 40% carbs
            self.target_protein = (self.target_calories * 0.30) / 4
            self.target_fat = (self.target_calories * 0.30) / 9
            self.target_carbs = (self.target_calories * 0.40) / 4

        self.save()
    

class FoodLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='food_logs')
    food_name = models.CharField(max_length=200)
    calories = models.FloatField()
    protein = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    log_date = models.DateField()

    def __str__(self):
        return f"{self.food_name} for {self.user.username} on {self.log_date}"