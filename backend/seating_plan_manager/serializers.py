from rest_framework import serializers
from .models import Student, SeatingPlan
from django.db import models

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class SeatingPlanSerializer(serializers.ModelSerializer):
    plan = serializers.PrimaryKeyRelatedField(queryset=SeatingPlan.objects.all(), many=True)
    plan = StudentSerializer(plan, many=True)

    class Meta:
        model = SeatingPlan
        fields = '__all__'