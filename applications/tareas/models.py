from django.db import models

class Task(models.Model):
    Titulo = models.CharField(max_length=100)
