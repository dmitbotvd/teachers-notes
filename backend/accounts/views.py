from django.urls import reverse
from rest_framework import generics, status, viewsets, permissions
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from accounts.models import User, Teacher, Student
from .serializers import (
    UserSerializer,
    TeacherSerializer,
    StudentSerializer,
    EmptySerializer,
    LoginSerializer,
)
from .tokens import account_activation_token
from .utils import generate_activation_token
import jwt
from django.conf import settings
from .models import User


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        current_site = get_current_site(self.request)
        mail_subject = "Activate your account."
        token = generate_activation_token(user)
        activation_link = (
            f"http://{current_site.domain}{reverse('activate')}?token={token}"
        )
        message = render_to_string(
            "accounts/activation_email.html",
            {
                "user": user,
                "activation_link": activation_link,
            },
        )
        to_email = serializer.validated_data.get("email")
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()


class RegisterTeacherView(generics.CreateAPIView):
    queryset = Teacher.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TeacherSerializer

    def perform_create(self, serializer):
        user_data = serializer.validated_data.pop("user")
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(is_active=False)
        teacher = serializer.save(user=user)
        current_site = get_current_site(self.request)
        mail_subject = "Activate your account."
        token = generate_activation_token(user)
        activation_link = (
            f"http://{current_site.domain}{reverse('activate')}?token={token}"
        )
        message = render_to_string(
            "accounts/activation_email.html",
            {
                "user": user,
                "activation_link": activation_link,
            },
        )
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return teacher


class RegisterStudentView(generics.CreateAPIView):
    queryset = Student.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = StudentSerializer

    def perform_create(self, serializer):
        user_data = serializer.validated_data.pop("user")
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(is_active=False)
        student = serializer.save(user=user)
        current_site = get_current_site(self.request)
        mail_subject = "Activate your account."
        token = generate_activation_token(user)
        activation_link = (
            f"http://{current_site.domain}{reverse('activate')}?token={token}"
        )
        message = render_to_string(
            "accounts/activation_email.html",
            {
                "user": user,
                "activation_link": activation_link,
            },
        )
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return student


class ActivateUserView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = EmptySerializer

    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload["user_id"])
        except jwt.ExpiredSignatureError:
            return Response(
                {"error": "Activation link has expired"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST
            )

        if user.is_active:
            return Response(
                {"message": "Account already activated"}, status=status.HTTP_200_OK
            )

        user.is_active = True
        user.save()
        return Response(
            {"message": "Account activated successfully"}, status=status.HTTP_200_OK
        )


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)


class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Teacher.objects.filter(user=self.request.user)


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)
