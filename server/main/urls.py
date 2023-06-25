from main import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'jobs', views.JobViewSet, basename='job')
router.register(r'tasks', views.TaskViewSet, basename='task')
#router.register(r'api-token-auth', obtain_auth_token, basename='api-token-auth')
# urlpatterns += [
#     path('api-token-auth/', views.obtain_auth_token)
# ]

urlpatterns = router.urls