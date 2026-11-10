from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Task
        exclude = ["usuario"]
        extra_kwargs = {
            "id": {"read_only": True},
            "fecha_creacion": {"read_only": True}
        }