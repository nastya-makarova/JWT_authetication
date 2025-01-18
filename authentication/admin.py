from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, RefreshTokenModel


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "email",
        "password",
        "created_at",
        "username"
    )

    list_editable = (
        "email",
        "username"
    )
    list_display_links = (
        "id",
    )
    ordering = ("id",)


@admin.register(RefreshTokenModel)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = (
        "refresh_token",
        "user",
        "created_at",
        "expired_at",
    )
