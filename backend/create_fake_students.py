import os
import django
from faker import Faker
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "xsettings.settings")
django.setup()

from accounts.models import User, Teacher, Student

fake = Faker()


def create_fake_students(num_students=10):
    # Получить учителя с указанным email
    teacher_email = "admin@i.ua"
    try:
        teacher_user = User.objects.get(email=teacher_email)
        teacher = Teacher.objects.get(user=teacher_user)
    except User.DoesNotExist:
        print(f"User with email {teacher_email} does not exist.")
        return
    except Teacher.DoesNotExist:
        print(f"Teacher associated with email {teacher_email} does not exist.")
        return

    for _ in range(num_students):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        username = fake.user_name()
        birth_date = fake.date_of_birth(minimum_age=18, maximum_age=22)
        gender = fake.random_element(elements=("M", "F"))
        grade = fake.random_element(
            elements=[
                "Elementary",
                "Beginner",
                "Intermediate",
                "Upper Intermediate",
                "Advanced",
                "Proficient",
            ]
        )
        phone_number = fake.phone_number()
        telegram_link = fake.url()

        user = User.objects.create(
            email=email,
            first_name=first_name,
            last_name=last_name,
            username=username,
            birth_date=birth_date,
            gender=gender,
            is_active=True,
        )
        user.set_password("password123")
        user.save()

        Student.objects.create(
            user=user,
            grade=grade,
            phone_number=phone_number,
            telegram_link=telegram_link,
            assigned_teacher=teacher,
        )


if __name__ == "__main__":
    create_fake_students()
