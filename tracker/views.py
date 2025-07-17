from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from datetime import datetime
from .models import UserProfile, FoodLog
from .serializers import UserProfileSerializer, FoodLogSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly



'''
for reference
https://www.django-rest-framework.org/api-guide/viewsets/#modelviewset
'''

# A ViewSet for the UserProfile model
class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_update(self, serializer):
        profile = serializer.save()
        # Recalculate goals when the profile is updated
        profile.calculate_goals()

# A ViewSet for the FoodLog model
class FoodLogViewSet(viewsets.ModelViewSet):
    queryset = FoodLog.objects.all()
    serializer_class = FoodLogSerializer
    permission_classes = [IsAuthenticated]

    # Users should only see their own food logs
    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        # Optional: filter by date if a 'date' query parameter is provided
        date_param = self.request.query_params.get('date')
        if date_param:
            queryset = queryset.filter(log_date=date_param)
        return queryset

    # When a new log is created, assign it to the current user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # A custom action to get the daily nutritional summary
    @action(detail=False, methods=['get'], url_path='summary')
    def summary(self, request):
        date_str = request.query_params.get('date', datetime.today().strftime('%Y-%m-%d'))

        # Filter logs for the current user and the specified date
        logs = self.get_queryset().filter(log_date=date_str)

        # Use Django's aggregation to calculate the sum of nutrients
        summary_data = logs.aggregate(
            total_calories=Sum('calories'),
            total_protein=Sum('protein'),
            total_fat=Sum('fat'),
            total_carbs=Sum('carbs')
        )

        return Response(summary_data, status=status.HTTP_200_OK)