from django.db import models
from accounts.models import Teacher, Student
from django.core.validators import FileExtensionValidator


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="lesson_images/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "png"])],
    )
    pdf = models.FileField(
        upload_to="lesson_pdfs/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["pdf"])],
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class LessonPlan(models.Model):
    teacher = models.ForeignKey(
        Teacher, on_delete=models.CASCADE, related_name="lesson_plans"
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="lesson_plans"
    )
    lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="lesson_plans"
    )
    date_assigned = models.DateField()
    due_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.lesson.title} for {self.student.user.first_name} {self.student.user.last_name}"
