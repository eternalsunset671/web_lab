from django.db import models
from django.urls import reverse

class Instructor(models.Model):
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')
    specialization = models.CharField(max_length=200, blank=True)
    degree = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Преподаватель'
        verbose_name_plural = 'Преподаватели'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Student(models.Model):
    FACULTY_CHOICES = [
        ('CS', 'Кибербезопасность'),
        ('SE', 'Программная инженерия'),
        ('IT', 'Информационные технологии'),
        ('DS', 'Наука о данных'),
        ('WEB', 'Веб-технологии'),
    ]

    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилия')
    email = models.EmailField(unique=True, verbose_name='Email')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    faculty = models.CharField(max_length=4, choices=FACULTY_CHOICES, default='CS', verbose_name='Факультет')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse('student_detail', kwargs={'pk': self.pk})


class Course(models.Model):
    LEVEL_CHOICES = [
        ('BEGINNER', 'Начальный'),
        ('INTERMEDIATE', 'Средний'),
        ('ADVANCED', 'Продвинутый'),
    ]

    title = models.CharField(max_length=200, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=200, unique=True, verbose_name='Слаг')
    description = models.TextField(blank=True, verbose_name='Описание')
    duration = models.PositiveIntegerField(default=0, verbose_name='Продолжительность (ч)')
    instructor = models.ForeignKey(Instructor, null=True, blank=True, on_delete=models.SET_NULL, related_name='courses')
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default='BEGINNER')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('course_detail', kwargs={'slug': self.slug})


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ('ACTIVE', 'Активен'),
        ('COMPLETED', 'Завершен'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')

    class Meta:
        verbose_name = 'Запись на курс'
        verbose_name_plural = 'Записи на курс'
        unique_together = ('student', 'course')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student} -> {self.course} ({self.status})"
