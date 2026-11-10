from django.db import models
from applications.users.models import User

class Task(models.Model):
    class Estado(models.IntegerChoices):
        PENDIENTE = 1, "Pendiente"
        EN_PROGRESO = 2, "En progreso"
        TERMINADA = 3, "Terminada"
        CANCELADA = 4, "Cancelada"

    titulo = models.CharField(max_length=100)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    estado = models.IntegerField(choices=Estado.choices, default=Estado.PENDIENTE)
