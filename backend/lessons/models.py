# lessons/models.py
from django.db import models
from students.models import Student


class Lesson(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    topic = models.CharField(max_length=200)
    homework = models.TextField(null=True, blank=True)
    plan = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Lesson'
        verbose_name_plural = 'Lessons'

    def __str__(self):
        return f"Lesson on {self.date} for {self.student.user.username}"
