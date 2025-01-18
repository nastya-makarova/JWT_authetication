from django.urls import include, path

from .views import (
    GetMeView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    RegisterView
)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("refresh/", RefreshTokenView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("me/", GetMeView.as_view())
]
