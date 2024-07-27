from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, Teacher, Student


class EmptySerializer(serializers.Serializer):
    pass


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

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

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Teacher
        fields = ["user", "subjects", "qualification", "experience"]


class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = [
            "user",
            "grade",
            "phone_number",
            "telegram_link",
            "assigned_teacher",
        ]


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        email = data.get("email")
        password = data.get("password")

        if email and password:
            user = authenticate(
                request=self.context.get("request"), email=email, password=password
            )
            if not user:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Must include both email and password")

        data["user"] = user
        return data
