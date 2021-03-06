from rest_framework import routers
from .api import StudentViewset, SeatingPlanViewset

router = routers.DefaultRouter()
router.register('api/students', StudentViewset, 'students')
router.register('api/plans', SeatingPlanViewset, 'plans')

urlpatterns = router.urls
