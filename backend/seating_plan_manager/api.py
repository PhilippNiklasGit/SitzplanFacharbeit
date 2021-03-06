from .models import Student, SeatingPlan
from rest_framework import viewsets, permissions
from .serializers import StudentSerializer, SeatingPlanSerializer

class StudentViewset(viewsets.ModelViewset):
    queryset = Student.objects.all()

    permission_classes = [
        permissions.AllowAny
    ]

    serializer_class = StudentSerializer

class SeatingPlanViewset(viewsets.ModelViewset):
    permission_classes = [
        permissions.IsAuthenticated
    ]

    serializer_class = SeatingPlanSerializer

    def get_queryset(self):
        return self.request.user.plans.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)