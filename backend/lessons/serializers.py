from rest_framework import serializers
from .models import Lesson, LessonPlan


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class LessonPlanTeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        fields = "__all__"


class LessonPlanStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPlan
        fields = "__all__"
        read_only_fields = (
            "teacher",
            "student",
            "lesson",
            "date_assigned",
            "due_date",
            "notes",
            "completed",
        )
