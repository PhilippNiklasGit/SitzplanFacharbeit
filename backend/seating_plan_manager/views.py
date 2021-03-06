from django.shortcuts import render
from rest_framework import viewsets
from .serializers import SeatingPlanSerializer
from .models import SeatingPlan

# Create your views here.
class SeatingPlanView(viewsets.ModelViewSet):
    serializer_class = SeatingPlanSerializer
    queryset = SeatingPlan.objects.all()