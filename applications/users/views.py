from drf_spectacular.utils import extend_schema
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from applications.users import serializers

from drf_spectacular.extensions import OpenApiAuthenticationExtension

class JWTCookieScheme(OpenApiAuthenticationExtension):
    # Asegúrate de que esta ruta sea EXACTAMENTE la que te aparece en el error de la consola
    target_class = 'applications.users.authentication.JWTCookieAuthentication'
    name = 'cookieAuth'

    def get_security_definition(self, auto_schema):
        return {
            'type': 'apiKey',
            'in': 'cookie',
            'name': 'access',  
        }

class LoginView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]  # pyrefly: ignore[bad-override-mutable-attribute]

    @extend_schema(
        summary="Login de usuario",
        description="Recibe el nombre de usuario y contraseña, si todo es correcto, devuelve los datos del usuario e injecta las cookies en la respuesta.",
        tags=["Autenticación"], # Agrupa este endpoint bajo la categoría "Autenticación" en Swagger
        request=serializers.CustomTokenObtainPairSerializer, # Le dice a Swagger qué campos debe mostrar en el formulario de envío
        responses={
            201: serializers.UserSerializer, # Si es exitoso, devuelve este serializador
        }
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.pop("access", None)
            refresh_token = response.data.pop("refresh", None)

            response.set_cookie(
                key="access",
                value=access_token,
                **settings.JWT_COOKIE_CONFIG,
            )

            if refresh_token:
                response.set_cookie(
                    key="refresh",
                    value=refresh_token,
                    **settings.JWT_COOKIE_CONFIG,
                )

        return response


class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Registrar un nuevo usuario",
        description="Recibe nombre de usuario, email y contraseña, si todo es correcto, devuelve los datos con los que se creo",
        tags=["Autenticación"], # Agrupa este endpoint bajo la categoría "Autenticación" en Swagger
        request=serializers.UserCreateSerializer, # Le dice a Swagger qué campos debe mostrar en el formulario de envío
        responses={
            201: serializers.UserSerializer, # Si es exitoso, devuelve este serializador
        }
    )
    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
        )

class MeView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Datos del usuario.",
        description="Lee el access token de la cookie para devolver los datos de ese usuario",
        tags=["Autenticación"], # Agrupa este endpoint bajo la categoría "Autenticación" en Swagger
        responses={
            201: serializers.UserSerializer, # Si es exitoso, devuelve este serializador
        }
    )
    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)

class LogoutView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        summary="Logout de usuario.",
        description="Elimina las cookies de access y refresh.",
        tags=["Autenticación"], # Agrupa este endpoint bajo la categoría "Autenticación" en Swagger
        request=None,
        responses={
            204: None, # Si es exitoso, devuelve este serializador
        }
    )
    def post(self, request):
        response = Response(
            status=status.HTTP_204_NO_CONTENT
        )
        response.delete_cookie("access", samesite=settings.JWT_COOKIE_CONFIG.get("samesite", "Lax"))
        response.delete_cookie("refresh", samesite=settings.JWT_COOKIE_CONFIG.get("samesite", "Lax"))
        return response

