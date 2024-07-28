from rest_framework import serializers
from accounts.models import Teacher, Student, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'avatar']


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ['user', 'subjects', 'qualification', 'experience']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            "id",
            "user",
            "grade",
            "phone_number",
            "telegram_link",
            "assigned_teacher",
        ]
        depth = 1  # To include related user fields
