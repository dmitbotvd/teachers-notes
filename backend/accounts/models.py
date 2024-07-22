from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
