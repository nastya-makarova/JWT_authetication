from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from .models import RefreshTokenModel

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email"
        )


class RegisterSerializer(serializers.ModelSerializer):
    """Serializer to registrate."""
    email = serializers.EmailField(
        required=True, max_length=254
    )
    password = serializers.CharField(       
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password"
        )

    def validate(self, data):
        user = User.objects.filter(email=data["email"]).first()
        if user:
            raise serializers.ValidationError(
                "The user already exists"
            )
        print(data)

        return data

    def to_representation(self, user):
        """The method modifies the serializer to display the User object.
        It is used when generating the response to a POST request."""
        serializer = UserSerializer(user)
        return serializer.data


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, max_length=254
    )
    password = serializers.CharField(       
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = (
            "email",
            "password"
        )

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return data


class RefreshTokenSerializer(serializers.ModelSerializer):

    class Meta:
        model = RefreshTokenModel
        fields = (
            "refresh_token",
        )

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            serializers.ValidationError(
                'An email address is required to log in.'
            )
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return data


class UserMeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        max_length=254,
    )
    username = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
        )
