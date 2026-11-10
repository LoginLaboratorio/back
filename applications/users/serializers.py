from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        data["username"] = self.user.username # pyrefly: ignore[missing-attribute]
        data["email"] = self.user.email # pyrefly: ignore[missing-attribute]
        data["role"] = self.user.role # pyrefly: ignore[missing-attribute]

        return data


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            email=validated_data.get("email"),
            password=validated_data["password"],
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "date_joined"]