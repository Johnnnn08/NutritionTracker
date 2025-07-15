from django.urls import path
from .views import search_food

urlpatterns = [
    path('foods/search/', search_food, name='search_food'),
]