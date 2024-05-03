from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    password_question = models.CharField(max_length=100, null=False, blank=False)
    
    
class PasswordQuestion(models.Model):
    question = models.CharField(max_length=100, null=False, blank=False)