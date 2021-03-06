from django.contrib import admin
from .models import Student, SeatingPlan

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('student_id', 'firstname', 'lastname')

class SeatingPlanAdmin(admin.ModelAdmin):
    list_display = ('plan_id', 'title')

admin.site.register(Student, StudentAdmin)
admin.site.register(SeatingPlan, SeatingPlanAdmin)
