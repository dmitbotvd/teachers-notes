from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from accounts.models import Teacher, Student
from accounts.serializers import TeacherSerializer, StudentSerializer
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404


class TeacherViewSet(viewsets.ViewSet):
    """Manage teachers and their students."""

    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["get"])
    def info(self, request):
        """Retrieve logged-in teacher's info."""
        teacher = Teacher.objects.get(user=request.user)
        serializer = TeacherSerializer(teacher)
        return Response(serializer.data)

    @action(detail=False, methods=["get", "post", "delete", "put"])
    def students(self, request):
        """Retrieve, add, delete, or update students for the logged-in teacher."""
        teacher = Teacher.objects.get(user=request.user)

        if request.method == "GET":
            students = teacher.students.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data)

        elif request.method == "POST":
            serializer = StudentSerializer(data=request.data)
            if serializer.is_valid():
                student = serializer.save(assigned_teacher=teacher)
                return Response(
                    StudentSerializer(student).data, status=status.HTTP_201_CREATED
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == "DELETE":
            user_id = request.data.get("user_id")
            try:
                student = Student.objects.get(user_id=user_id, assigned_teacher=teacher)
                student.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except Student.DoesNotExist:
                return Response(
                    {"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND
                )

        elif request.method == "PUT":
            user_id = request.data.get("user_id")
            student = get_object_or_404(
                Student, user_id=user_id, assigned_teacher=teacher
            )
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def student_detail(self, request, pk=None):
        """Retrieve a specific student by ID."""
        teacher = Teacher.objects.get(user=request.user)
        student = get_object_or_404(Student, user_id=pk, assigned_teacher=teacher)
        serializer = StudentSerializer(student)
        return Response(serializer.data)
