from rest_framework import serializers
from .models import User, Teacher, Student


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "username",
            "avatar",
            "birth_date",
            "gender",
        ]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ["user", "subjects", "qualification", "experience"]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        teacher, created = Teacher.objects.update_or_create(user=user, **validated_data)
        return teacher


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = [
            "user",
            "grade",
            "parent_contact",
            "enrollment_date",
            "assigned_teacher",
        ]

    def create(self, validated_data):
        user_data = validated_data.pop("user")
        user = UserSerializer.create(UserSerializer(), validated_data=user_data)
        student, created = Student.objects.update_or_create(user=user, **validated_data)
        return student
