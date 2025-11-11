from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404
from .forms import FeedbackForm, LoginForm, StudentRegistrationForm
from django.contrib import messages
from django.utils.html import escape
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, get_object_or_404, redirect
from .models import Student, Course, Instructor, Enrollment
from .forms import EnrollmentForm
from django.db import IntegrityError


def home_page(request):
    '''представление, которое рендерит шаблон index.html.'''
    total_students = Student.objects.filter(is_active=True).count()
    total_courses = Course.objects.filter(is_active=True).count()
    total_instructors = Instructor.objects.count()
    recent_courses = Course.objects.filter(is_active=True).order_by('-created_at')[:3]
    return render(request, 'university/index.html', {
        'title': 'Главная',
        'total_students': total_students,
        'total_courses': total_courses,
        'total_instructors': total_instructors,
        'recent_courses': recent_courses
    })


class AboutView(View):
    '''Class-Based Views для получения страницы О нас'''
    def get(self, request):
        return render(request, 'university/about.html', {})


def student_profile(request, pk):
    student = get_object_or_404(Student, pk=pk)
    enrollments = student.enrollments.select_related('course')
    return render(request, 'university/student_detail.html', {
        'student': student,
        'enrollments': enrollments
    })


class CourseListView(View):
    '''Страница со списком курсов'''
    def get(self, request):
        courses = Course.objects.filter(is_active=True).order_by('-created_at')
        return render(request, 'university/courses.html', {'courses': courses})


class CourseView(View):
    '''Страницы с курсами для динамической отрисовки'''
    def get(self, request, course_slug):
        course = get_object_or_404(Course, slug=course_slug)
        prev_course = Course.objects.filter(created_at__lt=course.created_at).order_by('-created_at').first()
        next_course = Course.objects.filter(created_at__gt=course.created_at).order_by('created_at').first()
        return render(request, 'university/course.html', {
            'course': course,
            'prev_course': prev_course,
            'next_course': next_course
        })
    
    
def custom_404(request, exception=None):
    '''специанльная страница для ошибки 404'''
    return render(request, 'university/not_found.html', status=404)
    

def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            message = f"Спасибо, {escape(data['name'])}! Ваше сообщение получено."
            return render(request, 'university/success.html', {'title': 'Сообщение отправлено', 'message': message})
    else:
        form = FeedbackForm()
    return render(request, 'university/feedback.html', {'form': form, 'title': 'Обратная связь'})


def register_view(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            student = form.save()
            return render(request, 'university/success.html', {'message': 'Вы успешно зарегистрированы!', 'student': student})
    else:
        form = StudentRegistrationForm()
    return render(request, 'university/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            return render(request, 'university/success.html', {
                'message': 'Вход выполнен успешно! Добро пожаловать в систему.',
                'title': 'Вход в систему'
            })
    else:
        form = LoginForm()
    
    return render(request, 'university/login.html', {
        'form': form,
        'title': 'Вход в систему'
    })


def contact(request):
    return render(request, 'university/contact.html')


def enroll_view(request):
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return render(request, 'university/success.html', {'message': 'Вы успешно записались на курс.'})
            except IntegrityError:
                form.add_error(None, 'Не удалось записать на курс (возможно уже есть запись).')
    else:
        form = EnrollmentForm()
    return render(request, 'university/enrollment.html', {'form': form})


def student_list(request):
    students = Student.objects.filter(is_active=True).order_by('last_name')
    return render(request, 'university/students.html', {'students': students})

