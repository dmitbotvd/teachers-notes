from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TeacherViewSet

router = DefaultRouter()
router.register(r"teacher", TeacherViewSet, basename="teacher")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "teacher/students/<int:pk>/",
        TeacherViewSet.as_view({"get": "student_detail"}),
        name="teacher-student-detail",
    ),
]
