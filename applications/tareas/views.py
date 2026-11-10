from drf_spectacular.utils import extend_schema, extend_schema_view
from rest_framework.viewsets import ModelViewSet
from applications.tareas import serializers as TareasSerializers
from applications.tareas import models as TareasModels
from rest_framework.permissions import IsAuthenticated

@extend_schema_view(
    list=extend_schema(
        summary="Listar tareas",
        description="Obtiene todas las tareas pertenecientes al usuario autenticado, ordenadas desde la más reciente.",
        tags=["Tareas"]
    ),
    create=extend_schema(
        summary="Crear una nueva tarea",
        description="Crea una tarea. El usuario autenticado se asigna automáticamente de forma interna.",
        tags=["Tareas"]
    ),
    retrieve=extend_schema(
        summary="Obtener detalle de una tarea",
        description="Devuelve los detalles de una tarea específica buscando por su ID.",
        tags=["Tareas"]
    ),
    update=extend_schema(
        summary="Actualizar tarea (Completo)",
        description="Actualiza todos los campos de una tarea específica.",
        tags=["Tareas"]
    ),
    partial_update=extend_schema(
        summary="Actualizar tarea (Parcial)",
        description="Actualiza uno o varios campos de una tarea sin necesidad de enviar todo el objeto.",
        tags=["Tareas"]
    ),
    destroy=extend_schema(
        summary="Eliminar una tarea",
        description="Elimina una tarea específica del usuario autenticado.",
        tags=["Tareas"]
    )
)
class TaskViewSet(ModelViewSet):
    queryset = TareasModels.Task.objects.all()
    
    serializer_class = TareasSerializers.TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TareasModels.Task.objects.filter(
            usuario=self.request.user
        ).order_by("-fecha_creacion")

    def perform_create(self, serializer):
        serializer.save(usuario=self.request.user)
