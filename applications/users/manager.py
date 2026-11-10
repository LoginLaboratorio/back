from django.db import models
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager, models.Manager):
    def _create_user(self, username, email, role, password, is_staff=False, is_superuser=False, **extra_fields):
        user = self.model(
            username=username,
            email=email,
            role=role,
            is_staff=is_staff,
            is_superuser=is_superuser,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, 1, password, True, True, **extra_fields)
    
    def create_user(self, username, email, password, **extra_fields):
        return self._create_user(username, email, 3, password, False, False, **extra_fields)