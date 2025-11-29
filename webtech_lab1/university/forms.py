from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Student, Enrollment

from django.contrib.auth.models import User
from .models import Student, Course, Enrollment, Instructor


class FeedbackForm(forms.Form):
    name = forms.CharField(
        label='Имя',
        min_length=2,
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ваше имя'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'})
    )
    subject = forms.CharField(
        label='Тема',
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        label='Сообщение',
        min_length=10,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 6})
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Email / Имя',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Введите пароль'})
    )


class RegistrationForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        label='Логин',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        max_length=100,
        label='Имя',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100,
        label='Фамилия',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    role = forms.ChoiceField(
        choices=[
            ('student', 'Студент'),
            ('instructor', 'Преподаватель'),
        ],
        label='Роль',
        widget=forms.Select(attrs={'class': 'form-control'})
    )


    def clean_username(self):
        username = self.cleaned_data['username']
        if len(username.strip()) < 3:
            raise ValidationError("Логин должен содержать минимум 3 символа")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Это имя пользователя уже занято")
        return username.strip()

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        if Student.objects.filter(email=email).exists():
            raise ValidationError('Студент с таким email уже существует.')
        return email

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get("password")
        pw2 = cleaned.get("password_confirm")

        if pw and pw2 and pw != pw2:
            raise ValidationError({'password_confirm': 'Пароли не совпадают'})

        return cleaned


class EnrollmentForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['student', 'course']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-select'}),
            'course': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        student = kwargs.pop('student', None)
        super(EnrollmentForm, self).__init__(*args, **kwargs)
        if student:
            self.fields['course'].queryset = Course.objects.filter(is_active=True).exclude(enrollment__student=student)
    
    
class GradeForm(forms.ModelForm):
    class Meta:
        model = Enrollment
        fields = ['grade', 'status', 'completed_date']
        widgets = {
            'completed_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'grade': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5}),
        }


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'birth_date', 'faculty', 'avatar', 'phone', 'description']
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'faculty': forms.Select(attrs={'class': 'form-control'}),
            'avatar': forms.FileInput(attrs={'class': 'form-control-file'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'duration', 'instructor', 'is_active']
        widgets = {
            'instructor': forms.Select(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }