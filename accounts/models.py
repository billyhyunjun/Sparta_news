from django.db import models
from django.contrib.auth.models import AbstractUser


class PasswordQuestion(models.Model):
    question = models.CharField(max_length=100, null=False, blank=False)


class User(AbstractUser):
    password_question = models.ForeignKey(
        PasswordQuestion, on_delete=models.CASCADE, null=True)
    password_answer = models.CharField(max_length=100, null=True)
