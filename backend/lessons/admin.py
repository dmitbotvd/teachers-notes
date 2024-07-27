from django.contrib import admin
from .models import Lesson, LessonPlan


class LessonAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "updated_at")
    search_fields = ("title",)
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)


class LessonPlanAdmin(admin.ModelAdmin):
    list_display = (
        "get_student_name",
        "get_teacher_name",
        "lesson",
        "date_assigned",
        "due_date",
        "completed",
    )
    search_fields = (
        "student__user__first_name",
        "student__user__last_name",
        "teacher__user__first_name",
        "teacher__user__last_name",
        "lesson__title",
    )
    list_filter = ("date_assigned", "due_date", "completed")
    ordering = ("-date_assigned",)

    def get_student_name(self, obj):
        return f"{obj.student.user.first_name} {obj.student.user.last_name}"

    get_student_name.short_description = "Student Name"

    def get_teacher_name(self, obj):
        return f"{obj.teacher.user.first_name} {obj.teacher.user.last_name}"

    get_teacher_name.short_description = "Teacher Name"


admin.site.register(Lesson, LessonAdmin)
admin.site.register(LessonPlan, LessonPlanAdmin)
