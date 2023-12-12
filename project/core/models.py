from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from djongo import models

# Create your models here.
class UserModel(models.Model):
    username = models.TextField(max_length=100)
    password = models.TextField(max_length=100)

    class Meta:
        app_label = 'core'