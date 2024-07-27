from django.db import models
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True, null=True, blank=True)
    avatar = models.ImageField(
        upload_to="avatars/",
        validators=[FileExtensionValidator(["jpg", "png"])],
        blank=True,
        null=True,
    )
    birth_date = models.DateField(blank=True, null=True)
    gender = models.CharField(
        max_length=10, choices=[("M", "Male"), ("F", "Female")], blank=True, null=True
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subjects = models.CharField(max_length=255, blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True, null=True)
    experience = models.PositiveIntegerField(default=0)  # in years

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    grade = models.CharField(max_length=10, blank=True, null=True)
    parent_contact = models.CharField(max_length=255, blank=True, null=True)
    enrollment_date = models.DateField(blank=True, null=True)
    assigned_teacher = models.ForeignKey(
        Teacher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="students",
    )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
