from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import UserProfile


class FeedbackForm(forms.Form):
    '''
    Класс для обработки формы обратной связи и валидации
    1. Валидация имени
    2. Валидации названия почты
    '''
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

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 2:
            raise ValidationError('Имя должно содержать минимум 2 символа')
        return name

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        try:
            validate_email(email)
        except ValidationError:
            raise ValidationError('Некорректный email')
        return email


class RegistrationForm(forms.Form):
    '''
    Класс для обработки формы обратной связи и валидации
    1. Валидация имени.
    2. Валидации названия почты.
    3. Валидации названия пароля.
    4. Валидации при подтверждении пароля.
    '''
    username = forms.CharField(
        label='Логин',
        min_length=3,
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'you@example.com'})
    )
    password = forms.CharField(
        label='Пароль',
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'})
    )
    password_confirm = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Повторите пароль'})
    )

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if len(username) < 2:
            raise ValidationError('Логин должен содержать минимум 2 символа')
        if UserProfile.objects.filter(username__iexact=username).exists():
            raise ValidationError('Пользователь с таким логином уже существует')
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if UserProfile.objects.filter(email__iexact=email).exists():
            raise ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise ValidationError('Пароль должен содержать минимум 8 символов')
        if password.isdigit() or password.isalpha():
            raise ValidationError('Пароль должен содержать буквы и цифры (и желательно спецсимволы)')
        return password

    def clean(self):
        cleaned = super().clean()
        pw = cleaned.get('password')
        pwc = cleaned.get('password_confirm')
        if pw and pwc and pw != pwc:
            raise ValidationError({'password_confirm': 'Пароли не совпадают'})
        return cleaned


class LoginForm(forms.Form):
    username = forms.CharField(
        label='Имя пользователя',
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введите пароль'
        })
    )

