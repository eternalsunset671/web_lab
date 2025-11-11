from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Student, Enrollment


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


class StudentRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Student
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'faculty']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'faculty': forms.Select(attrs={'class': 'form-select'}),
        }

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

    def clean(self):
        cleaned = super().clean()
        student = cleaned.get("student")
        course = cleaned.get("course")

        if student and course:
            if Enrollment.objects.filter(student=student, course=course).exists():
                raise ValidationError("Студент уже записан на этот курс.")

        return cleaned
