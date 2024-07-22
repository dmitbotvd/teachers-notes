from django.db import models
from accounts.models import User
from teachers.models import Teacher

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    grade = models.CharField(max_length=10)

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return self.user.username
