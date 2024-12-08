from django.contrib.auth import get_user_model
from django.forms.utils import from_current_timezone
from rest_framework import status as st
from rest_framework.authentication import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from authapp.utils import get_tokens_for_user
from authapp.permissions import IsOwner

from .models import User

from .serializers import (
    ProfileSerializer,
    LoginSerializer,
    RegistrationSerializer,
)


class RegisterView(APIView):

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response_dict = {
            "user": {"email": user.email, "full_name": user.full_name},
            "msg": "Registration successful",
        }
        return Response(response_dict, status=st.HTTP_201_CREATED)


class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        tokens = get_tokens_for_user(user)

        return Response(
            {"user": {"email": user.email , "full_name": user.full_name} ,"tokens": tokens, "msg": "Login successful"}, status=st.HTTP_200_OK
        )


class ProfileView(ModelViewSet):
    serializer_class = ProfileSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        self.check_object_permissions(self.request, self.request.user)
        return self.request.user

    def list(self, request, *args, **kwargs):
        user = self.get_object()
        ser = self.get_serializer(user)
        return Response(ser.data)

    def update(self, request, *args, **kwargs):
        return self._update_profile(request.data, partial=False)

    def partial_update(self, request, *args, **kwargs):
        return self._update_profile(request.data, partial=True)

    def _update_profile(self, data, partial):
        # logic for both update and partial_update
        data = data.copy()
        if "email" in data:
            data.pop("email")

        serializer = self.get_serializer(
            self.get_object(), data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class ChangePasswordView(APIView):
    pass


class SendPasswordResetEmailView(APIView):
    pass


class PasswordResetView(APIView):
    pass
