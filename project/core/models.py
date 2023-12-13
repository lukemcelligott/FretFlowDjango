from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from djongo import models
from django.contrib.auth.hashers import make_password

# Create your models here.
class UserModel(models.Model):
    username = models.TextField(max_length=100)
    password = models.TextField(max_length=100)

    class Meta:
        app_label = 'core'

    def save(self, *args, **kwargs):
    # Hash the password before saving
        if self.password:  # Ensure there's a password before hashing
            self.password = make_password(self.password)
        super().save(*args, **kwargs)