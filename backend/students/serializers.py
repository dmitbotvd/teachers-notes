from rest_framework import serializers
from accounts.models import Student


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["user", "teacher", "grade"]
