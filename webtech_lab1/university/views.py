from django.shortcuts import render, redirect
from django.views import View
from django.http import Http404
from .forms import FeedbackForm, RegistrationForm, LoginForm
from .models import UserProfile
from django.contrib import messages
from django.utils.html import escape
from django.contrib.auth.hashers import make_password

STUDENTS_DATA = {
    1: {'info': 'Иван Петров', 'faculty': 'Кибербезопасность', 'status': 'Активный', 'year': 3},
    2: {'info': 'Мария Сидорова', 'faculty': 'Информатика', 'status': 'Активный', 'year': 2},
    3: {'info': 'Алексей Козлов', 'faculty': 'Программная инженерия', 'status': 'Выпускник', 'year': 5}
}


def home_page(request):
    '''представление, которое рендерит шаблон index.html.'''
    return render(request, 'university/index.html', {})


class AboutView(View):
    '''Class-Based Views для получения страницы О нас'''
    def get(self, request):
        return render(request, 'university/about.html', {})


def student_profile(request, student_id):
    '''представление, которое рендерит страницы шаблонов динамически 
    для студентов с номерами от 1 до 100, иначе возвращает 404
    и кнопки переходов между страницами студентов '''
    if student_id > 100 or student_id < 1 or student_id not in STUDENTS_DATA:
        return render(request, 'university/not_found.html', status=404)
    if student_id in STUDENTS_DATA:
        student_data = STUDENTS_DATA[student_id]
        return render(request, 'university/student.html', {
            'student_id': student_id,
            'info': student_data['info'],
            'faculty': student_data['faculty'],
            'status': student_data['status'],
            'year': student_data['year'],
            'prev_id': student_id - 1 if student_id > 1 else None,
            'next_id': student_id + 1 if student_id < 100 else None,
        })
    else:
        raise Http404("Студент с таким ID не найден")

class CourseListView(View):
    '''Страница со списком курсов'''
    def get(self, request):
        courses = CourseView.COURSES
        context = {'courses': courses}
        return render(request, 'university/courses.html', context)


class CourseView(View):
    '''Страницы с курсами для динамической отрисовки'''
    COURSES = {
        'python-basics': {'name': 'Основы программирования на Python', 'duration': 36, 'description': 'Базовый курс...', 'instructor': 'Доцент Петров И.С.', 'level': 'Начальный'},
        'web-security': {'name': 'Веб-безопасность', 'duration': 48, 'description': 'Курс по защите веб-приложений', 'instructor': 'Профессор Сидоров А.В.', 'level': 'Продвинутый'},
        'network-defense': {'name': 'Защита сетей', 'duration': 42, 'description': 'Методы защиты сетей', 'instructor': 'Доцент Козлова М.П.', 'level': 'Средний'}
    }
    
    def get(self, request, course_slug):
        course = self.COURSES.get(course_slug)
        if not course:
            raise Http404('Курс не найден')

        # Список слагов в порядке определения
        slugs = list(self.COURSES.keys())
        index = slugs.index(course_slug)

        # Определяем соседние курсы
        prev_slug = slugs[index - 1] if index > 0 else None
        next_slug = slugs[index + 1] if index < len(slugs) - 1 else None

        context = {
            'course_slug': course_slug,
            'title': course,
            'prev_slug': prev_slug,
            'next_slug': next_slug,
            'courses': self.COURSES
        }
        return render(request, 'university/course.html', context)
    
    
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
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            hashed_pw = make_password(data['password'])
            user = UserProfile.objects.create(username=data['username'], email=data['email'], password=hashed_pw)
            message = f"Пользователь {escape(user.username)} успешно зарегистрирован."
            return render(request, 'university/success.html', {'title': 'Регистрация успешна', 'message': message})
    else:
        form = RegistrationForm()
    return render(request, 'university/register.html', {'form': form, 'title': 'Регистрация'})


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

