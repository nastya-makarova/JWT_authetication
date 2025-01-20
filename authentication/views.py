from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import RefreshTokenModel
from .serializers import (
    LoginSerializer,
    RefreshTokenSerializer,
    RegisterSerializer,
    UserMeSerializer
)
from .service import generate_access_token, generate_refersh_token

User = get_user_model()


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
        token = generate_access_token(user)
        try:
            refresh_token = RefreshTokenModel.objects.get(user=user)
        except ObjectDoesNotExist:
            refresh_token = None
        if refresh_token is None or refresh_token.expired_at < timezone.now():
            if refresh_token:
                refresh_token.delete()

            refresh_token, expired_at = generate_refersh_token(user)
            RefreshTokenModel.objects.create(
                user=user,
                refresh_token=refresh_token,
                expired_at=expired_at
            )

        return Response({"access_token": token}, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (AllowAny,)

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        try:
            refresh_token_obj = RefreshTokenModel.objects.get(
                refresh_token=refresh_token
            )
            if refresh_token_obj.expired_at < timezone.now():
                return Response({'error': 'Refresh token expired'}, status=400)

            new_access_token = generate_access_token(refresh_token_obj.user)
            return Response({
                'access_token': new_access_token
            })
        except Exception as e:
            return Response({'error': str(e)}, status=400)


class LogoutView(APIView):
    serializer_class = RefreshTokenSerializer
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(request_body=RefreshTokenSerializer)
    def post(self, request):
        refresh_token = request.data.get('refresh_token')
        try:
            refresh_token_obj = RefreshTokenModel.objects.get(
                refresh_token=refresh_token
            )
            refresh_token_obj.delete()
            return Response({'success': 'User logged out.'})
        except RefreshTokenModel.DoesNotExist:
            return Response({'error': 'Invalid refresh token'}, status=400)


class GetMeView(APIView):
    permission_classes = (IsAuthenticated,)

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_QUERY, description="Name of the user", type=openapi.TYPE_INTEGER),
            openapi.Parameter('username', openapi.IN_QUERY, type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_QUERY, type=openapi.TYPE_STRING)
        ],
        responses={
            200: UserMeSerializer
        }
    )
    def get(self, request):
        user = request.user
        serializer = UserMeSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(request_body=UserMeSerializer)
    def put(self, request):
        user = request.user
        serializer = UserMeSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
