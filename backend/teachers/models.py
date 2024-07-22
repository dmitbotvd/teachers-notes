
from django.db import models
from accounts.models import User

class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    subjects = models.CharField(max_length=200)

    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return self.user.username
