from django.contrib import admin
from .models import Teacher, Student, User


class TeacherInline(admin.StackedInline):
    model = Teacher
    can_delete = False
    fields = ["subjects", "qualification", "experience"]
    extra = 0


class StudentInline(admin.StackedInline):
    model = Student
    can_delete = False
    fields = ["grade", "phone_number", "telegram_link", "assigned_teacher"]
    extra = 0


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "is_staff", "is_active")
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_staff", "is_active")
    ordering = ("email",)
    inlines = [TeacherInline, StudentInline]


admin.site.register(User, CustomUserAdmin)


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

    def get_queryset(self, request):
        return super().get_queryset(request).select_related("user")


class StudentAdmin(admin.ModelAdmin):
    list_display = (
        "get_email",
        "get_first_name",
        "get_last_name",
        "grade",
        "phone_number",
        "telegram_link",
        "assigned_teacher",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "grade",
        "assigned_teacher__user__first_name",
        "assigned_teacher__user__last_name",
    )
    list_filter = ("grade",)
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

    def get_queryset(self, request):
        return (
            super()
            .get_queryset(request)
            .select_related("user", "assigned_teacher__user")
        )


admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Student, StudentAdmin)
