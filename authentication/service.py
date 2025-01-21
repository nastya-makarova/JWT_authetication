from datetime import timedelta
import jwt
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


# The function to generate an access token.
def generate_access_token(user):
    dt = timezone.now() + timedelta(
        seconds=settings.CONSTANCE_CONFIG["ACCESS_TOKEN_LIFESPAN"]
    )
    payload = {
        "user_id": user.id,
        "expires_at": int(dt.strftime('%s'))
    }
    access_token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return access_token


# The function to generate an refresh token.
def generate_refersh_token(user):
    refresh_token = uuid.uuid4()
    expired_at = timezone.now() + timedelta(
        days=settings.CONSTANCE_CONFIG["REFRESH_TOKEN_LIFESPAN"]
    )
    return refresh_token, expired_at
