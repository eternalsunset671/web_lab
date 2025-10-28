from django.db import models
from django.core.validators import MinLengthValidator


class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"{self.username} <{self.email}>"