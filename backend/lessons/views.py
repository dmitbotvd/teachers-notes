from rest_framework import viewsets, permissions, filters
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Lesson, LessonPlan
from .serializers import (
    LessonSerializer,
    LessonPlanTeacherSerializer,
    LessonPlanStudentSerializer,
)
from .permissions import IsTeacher, IsStudentOrTeacher
from .filters import LessonPlanFilter
from accounts.models import Teacher, Student


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated, IsTeacher]


class LessonPlanViewSet(viewsets.ModelViewSet):
    queryset = LessonPlan.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = LessonPlanFilter
    search_fields = ["lesson__title", "notes"]
    ordering_fields = ["date_assigned", "due_date", "completed"]
    permission_classes = [permissions.IsAuthenticated, IsStudentOrTeacher]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return LessonPlanTeacherSerializer
        return LessonPlanStudentSerializer

    def get_queryset(self):
        if self.request.user.is_staff:
            return LessonPlan.objects.filter(teacher__user=self.request.user)
        return LessonPlan.objects.filter(student__user=self.request.user)

    def perform_create(self, serializer):
        if self.request.user.is_staff:
            teacher = Teacher.objects.get(user=self.request.user)
            serializer.save(teacher=teacher)
        else:
            raise PermissionDenied("Only teachers can create lesson plans.")

    def perform_update(self, serializer):
        if self.request.user.is_staff:
            serializer.save()
        else:
            raise PermissionDenied("Only teachers can update lesson plans.")

    def perform_destroy(self, instance):
        if self.request.user.is_staff:
            instance.delete()
        else:
            raise PermissionDenied("Only teachers can delete lesson plans.")


class CurrentLessonViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Lesson.objects.filter(
                lesson_plans__teacher__user=self.request.user
            ).distinct()
        return Lesson.objects.filter(
            lesson_plans__student__user=self.request.user
        ).distinct()
