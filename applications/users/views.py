from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from applications.users import serializers


class LoginView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    permission_classes = []  # pyrefly: ignore[bad-override-mutable-attribute]

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

    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "User created successfully."},
            status=status.HTTP_201_CREATED,
        )


class MeView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        serializer = serializers.UserSerializer(request.user)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        response = Response(
            {"message": "Logged out successfully."},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie("access", samesite=settings.JWT_COOKIE_CONFIG.get("samesite", "Lax"))
        response.delete_cookie("refresh", samesite=settings.JWT_COOKIE_CONFIG.get("samesite", "Lax"))
        return response

