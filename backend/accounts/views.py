from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .models import User, Teacher, Student
from .serializers import UserSerializer, TeacherSerializer, StudentSerializer
from .tokens import account_activation_token


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=False)
        current_site = get_current_site(self.request)
        mail_subject = "Activate your account."
        message = render_to_string(
            "accounts/activation_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
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
        user_data = serializer.validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(is_active=False)
        teacher = serializer.save(user=user)
        current_site = get_current_site(self.request)
        mail_subject = "Activate your account."
        message = render_to_string(
            "accounts/activation_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
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
        user_data = serializer.validated_data.pop('user')
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save(is_active=False)
        student = serializer.save(user=user)
        current_site = get_current_site(self.request)
        mail_subject = "Activate your account."
        message = render_to_string(
            "accounts/activation_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        to_email = user.email
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return student


class ActivateUserView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return Response(
                {
                    "message": "Thank you for your email confirmation. Now you can login your account."
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"error": "Activation link is invalid!"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(generics.GenericAPIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )


class LogoutView(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response(status=status.HTTP_204_NO_CONTENT)
