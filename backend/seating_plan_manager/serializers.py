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

    def create(self, validated_data):
        title = validated_data.pop('title')
        new_plan = SeatingPlan.objects.create(title=title)
        new_plan.save()

        new_board = []
        new_board_student = []
        
        for i in validated_data:
            new_board.append(dict(i))
        
        for i in new_board:
            new_student = Student(tablename=i['tablename'], firstname=i['firstname'], lastname=i['lastname'])
            new_student.save()
            new_board_student.append(new_student)
        
        new_plan.plan.set(new_board_student)

        return new_plan

    def update(self, instance, validated_data):
        new_board = []

        for i in validated_data['plan']:
            new_board.append(dict(i))
        
        for i in new_board:
            updated_student = instance.plan.filter(tablename=i['tablename']).update(firstname=i['firstname'], lastname=i['lastname'])

            if updated_student==0:
                new_student = Student(firstname=i['firstname'], lastname=i['lastname'], tablename=i['tablename'])
                new_student.save()
                instance.save()
                instance.plan.add(new_student)
        
        return instance