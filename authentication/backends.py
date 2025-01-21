import jwt

from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework import authentication, exceptions

User = get_user_model()


class JWTAuthentication(authentication.BaseAuthentication):
    authentication_header_prefix = 'Bearer'

    def authenticate(self, request):
        request.user = None

        auth_header = authentication.get_authorization_header(request).split()
        auth_header_prefix = self.authentication_header_prefix.lower()

        if not auth_header:
            return None

        if len(auth_header) == 1:
            return None

        elif len(auth_header) > 2:
            return None

        prefix = auth_header[0].decode('utf-8')
        token = auth_header[1].decode('utf-8')

        if prefix.lower() != auth_header_prefix:
            return None

        return self.authenticate_credentials(request, token)

    def authenticate_credentials(self, request, token):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms='HS256'
            )
            print(payload)
        except Exception:
            msg = "Authentication error."
            raise exceptions.AuthenticationFailed(msg)

        try:
            user = User.objects.get(pk=payload['user_id'])
        except User.DoesNotExist:
            msg = "User corresponding to this token was not found."
            raise exceptions.AuthenticationFailed(msg)

        if not user.is_active:
            msg = "User inactive."
            raise exceptions.AuthenticationFailed(msg)

        return (user, token)
