from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.forms import ValidationError
from rest_framework import serializers

from .models import User


class RegistrationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["email", "full_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        try:
            # validate passowrd using django validators
            validate_password(attrs.get("password"))
        except ValidationError as e:
            # re-raise errors associated with password field
            raise serializers.ValidationError({"password": e.messages})
        return attrs

    def create(self, validated_data):
        """
        Create and return  new user instance with a hashed password 
        """
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # authenticate user
        user = authenticate(email=email, password=password)
        if not user:
            raise serializers.ValidationError(
                {"non_field_errors": ["Invalid Credentials!"]}
            )
        if not user.is_active:
            raise serializers.ValidationError(
                {"non_field_errors": ["Account is not active!"]}
            )

        attrs["user"] = user
        return attrs


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "full_name",
            "bio",
            "date_joined",
            "last_login",
        )
        read_only_fields = ("email", "date_joined", "last_login")
