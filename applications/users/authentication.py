from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTCookieAuthentication(JWTAuthentication):
    
    def authenticate(self, request):
        # Intentar leer el token desde la cookies
        raw_token = request.COOKIES.get("access")

        # Si no hay cookie, intentar el metodo tradicional
        if raw_token is None:
            return super().authenticate(request)
        
        # Valida el token y obtiene el usuario
        validated_token = self.get_validated_token(raw_token)
        return self.get_user(validated_token), validated_token    