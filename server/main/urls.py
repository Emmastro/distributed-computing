from main import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'jobs', views.JobViewSet, basename='job')
router.register(r'tasks', views.TaskViewSet, basename='task')

urlpatterns = router.urls