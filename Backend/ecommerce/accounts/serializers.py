# serializers.py
import random
import string
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, min_length=6)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        if not username:
            raise serializers.ValidationError({"email": "username is required."})

        if not email:
            raise serializers.ValidationError({"email": "Email is required."})

        if password:
            if User.objects.filter(email=email).exists():
                raise serializers.ValidationError({"email": "This email is already registered."})
            if password != confirm_password:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
            try:
                validate_password(password)
            except ValidationError as e:
                raise serializers.ValidationError({"password": e.messages})

        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password', None)
        password = validated_data.pop('password', None)
        email = validated_data['email']

        user = User.objects.filter(email=email).first() if password is None else None
        if user:
            return user

        user = User(
            username=validated_data['username'],
            email=email,
            is_active=False if password else True
        )

        user.set_password(password or ''.join(random.choices(string.ascii_letters + string.digits, k=12)))
        user.save()
        return user
