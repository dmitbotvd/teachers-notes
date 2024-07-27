from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, LessonPlanViewSet

router = DefaultRouter()
router.register(r"lessons", LessonViewSet, basename="lesson")
router.register(r"lesson-plans", LessonPlanViewSet, basename="lesson-plan")

urlpatterns = [
    path("", include(router.urls)),
]
