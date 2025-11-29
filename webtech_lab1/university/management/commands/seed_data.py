from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from university.models import Student, Instructor, Course, Enrollment
from datetime import date

class Command(BaseCommand):
    help = 'Заполняет базу данных тестовыми данными'

    def handle(self, *args, **options):
        self.stdout.write('Создание тестовых данных...')

        Enrollment.objects.all().delete()
        Course.objects.all().delete()
        Student.objects.all().delete()
        Instructor.objects.all().delete()
        User.objects.filter(is_staff=False).delete()

        instructors_data = [
            {
                'first_name': 'Иван',
                'last_name': 'Петров',
                'email': 'i.petrov@fefu.ru',
                'specialization': 'Кибербезопасность',
                'degree': 'Кандидат технических наук'
            },
            {
                'first_name': 'Мария',
                'last_name': 'Сидорова',
                'email': 'm.sidorova@fefu.ru',
                'specialization': 'Веб-разработка',
                'degree': 'Доктор технических наук'
            },
            {
                'first_name': 'Алексей',
                'last_name': 'Козлов',
                'email': 'a.kozlov@fefu.ru',
                'specialization': 'Сетевые технологии',
                'degree': ''
            },
        ]

        instructors = []
        for data in instructors_data:
            user = User.objects.create_user(
                username=data['email'].split('@')[0],
                email=data['email'],
                password='password123'
            )
            instructor = Instructor.objects.create(
                user=user,
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                specialization=data['specialization'],
                degree=data['degree']
            )
            instructors.append(instructor)

        students_data = [
            {'first_name': 'Анна', 'last_name': 'Иванова', 'email': 'anna.ivanova@fefu.ru', 'birth_date': date(2000, 5, 15), 'faculty': 'CS'},
            {'first_name': 'Дмитрий', 'last_name': 'Смирнов', 'email': 'dmitry.smirnov@fefu.ru', 'birth_date': date(1999, 8, 22), 'faculty': 'SE'},
            {'first_name': 'Екатерина', 'last_name': 'Попова', 'email': 'ekaterina.popova@fefu.ru', 'birth_date': date(2001, 3, 10), 'faculty': 'IT'},
            {'first_name': 'Михаил', 'last_name': 'Васильев', 'email': 'mikhail.vasilyev@fefu.ru', 'birth_date': date(2000, 11, 5), 'faculty': 'DS'},
            {'first_name': 'Ольга', 'last_name': 'Новикова', 'email': 'olga.novikova@fefu.ru', 'birth_date': date(1999, 12, 30), 'faculty': 'WEB'},
        ]

        students = []
        for data in students_data:
            user = User.objects.create_user(
                username=data['email'].split('@')[0],
                email=data['email'],
                password='password123'
            )
            student = Student.objects.create(
                user=user,
                first_name=data['first_name'],
                last_name=data['last_name'],
                email=data['email'],
                birth_date=data['birth_date'],
                faculty=data['faculty']
            )
            students.append(student)

        courses_data = [
            {'title': 'Основы Python', 'slug': 'python-basics', 'description': 'Базовый курс по программированию на языке Python. Изучение синтаксиса, структур данных и основ ООП.', 'duration': 36, 'instructor': instructors[0], 'level': 'BEGINNER'},
            {'title': 'Веб-безопасность', 'slug': 'web-security', 'description': 'Продвинутый курс по защите веб-приложений. SQL-инъекции, XSS, CSRF и другие уязвимости.', 'duration': 48, 'instructor': instructors[0], 'level': 'ADVANCED'},
            {'title': 'Современный JavaScript', 'slug': 'modern-javascript', 'description': 'Изучение современных возможностей JavaScript: ES6+, асинхронное программирование, фреймворки.', 'duration': 42, 'instructor': instructors[1], 'level': 'INTERMEDIATE'},
            {'title': 'Защита сетей', 'slug': 'network-defense', 'description': 'Курс по защите компьютерных сетей. Firewalls, IDS/IPS, VPN и методы атак на сети.', 'duration': 40, 'instructor': instructors[2], 'level': 'ADVANCED'},
        ]

        courses = []
        for data in courses_data:
            course = Course.objects.create(**data)
            courses.append(course)

        enrollments_data = [
            {'student': students[0], 'course': courses[0], 'status': 'ACTIVE'},
            {'student': students[0], 'course': courses[1], 'status': 'ACTIVE'},
            {'student': students[1], 'course': courses[0], 'status': 'ACTIVE'},
            {'student': students[1], 'course': courses[2], 'status': 'ACTIVE'},
            {'student': students[2], 'course': courses[0], 'status': 'ACTIVE'},
            {'student': students[3], 'course': courses[3], 'status': 'ACTIVE'},
            {'student': students[4], 'course': courses[2], 'status': 'ACTIVE'},
        ]

        for data in enrollments_data:
            Enrollment.objects.create(**data)

        self.stdout.write(
            self.style.SUCCESS(
                f'Успешно создано: {len(instructors)} преподавателей, '
                f'{len(students)} студентов, {len(courses)} курсов, '
                f'{len(enrollments_data)} записей на курсы'
            )
        )
