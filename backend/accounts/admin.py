# accounts/admin.py

from django.contrib import admin
from .models import Teacher, Student


class TeacherAdmin(admin.ModelAdmin):
    list_display = (
        "get_email",
        "get_first_name",
        "get_last_name",
        "subjects",
        "qualification",
        "experience",
    )
    search_fields = ("user__first_name", "user__last_name", "subjects")
    list_filter = ("qualification", "experience")
    ordering = ("user__last_name", "user__first_name")

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "Email"

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = "First Name"

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = "Last Name"


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "get_email",
        "get_first_name",
        "get_last_name",
        "grade",
        "parent_contact",
        "enrollment_date",
        "assigned_teacher",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "grade",
        "assigned_teacher__user__first_name",
        "assigned_teacher__user__last_name",
    )
    list_filter = ("grade", "enrollment_date")
    ordering = ("user__last_name", "user__first_name")

    def get_email(self, obj):
        return obj.user.email

    get_email.short_description = "Email"

    def get_first_name(self, obj):
        return obj.user.first_name

    get_first_name.short_description = "First Name"

    def get_last_name(self, obj):
        return obj.user.last_name

    get_last_name.short_description = "Last Name"


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
