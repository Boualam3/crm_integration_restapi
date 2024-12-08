from rest_framework.routers import DefaultRouter
from django.urls import path, include

from . import views

router = DefaultRouter()

router.register("profile", views.ProfileView, basename="profile")


urlpatterns = [
    path("register/", views.RegisterView.as_view()),
    path("login/", views.LoginView.as_view(), name="login"),

    path(
        "changepassword/", views.ChangePasswordView.as_view(), name="changepassword"
    ),
    path(
        "send-reset-password-email/",
        views.SendPasswordResetEmailView.as_view(),
        name="send-reset-password-email",
    ),
    path(
        "reset-password/<uid>/<token>/",
        views.PasswordResetView.as_view(),
        name="resetpassword",
    ),
]

# include profile endpoints
urlpatterns += [
    path("", include(router.urls)),
]
