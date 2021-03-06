from django.db import models
import uuid

from django.contrib.auth.models import User

# Create your models here.
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    tablename = models.CharField(max_length=2, null=True)
    firstname = models.CharField(max_length=120)
    lastname = models.CharField(max_length=120)

    def _str_(self):
        return self.firstname + self.lastname

class SeatingPlan(models.Model):
    plan_id = models.AutoField(primary_key=True, default=None)
    title = models.CharField(max_length=120, blank=True)
    plan = models.ManyToManyField('Student', blank=True)
    owner = models.ForeignKey(User, related_name="plans", on_delete=models.CASCADE, null=True)

    def _str_(self):
        return self.title
