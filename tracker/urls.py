from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, FoodLogViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet, basename='userprofile')
router.register(r'logs', FoodLogViewSet, basename='foodlog')


urlpatterns = [
    path('', include(router.urls)),
]