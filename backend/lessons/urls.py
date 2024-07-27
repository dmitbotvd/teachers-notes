from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LessonViewSet, LessonPlanViewSet, CurrentLessonViewSet

router = DefaultRouter()
router.register(r"lessons", LessonViewSet, basename="lesson")
router.register(r"lesson-plans", LessonPlanViewSet, basename="lesson-plan")
router.register(r"current-lessons", CurrentLessonViewSet, basename="current-lesson")

urlpatterns = [
    path("", include(router.urls)),
]
