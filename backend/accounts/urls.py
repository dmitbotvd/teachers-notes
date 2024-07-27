# accounts/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    RegisterUserView,
    RegisterTeacherView,
    RegisterStudentView,
    LoginView,
    LogoutView,
    ActivateUserView,
    UserViewSet,
    TeacherViewSet,
    StudentViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")
router.register(r"teachers", TeacherViewSet, basename="teacher")
router.register(r"students", StudentViewSet, basename="student")
urlpatterns = [
    path("activate/", ActivateUserView.as_view(), name="activate"),
    path("register/", RegisterUserView.as_view(), name="register"),
    path("register/teacher/", RegisterTeacherView.as_view(), name="register_teacher"),
    path("register/student/", RegisterStudentView.as_view(), name="register_student"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
    path("", include(router.urls)),
]
