from rest_framework import serializers
from .models import Lesson


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "student",
            "date",
            "start_time",
            "end_time",
            "topic",
            "homework",
            "plan",
        ]
