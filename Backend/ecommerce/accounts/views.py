from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from .serializers import RegisterSerializer


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.is_active = True
            user.save()

          
            print("user email ",user.email)
            send_mail(
                subject="Welcome to Bull Wheels! 🚗",
                message=f"""
            Hi {user.username},

            Welcome to Bull Wheels! We're excited to have you on board.

            Enjoy exploring our website and all the amazing wheels we have for you!

            Thanks,
            The Bull Wheels Team
            """,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=True
            )

            return Response(
                {"message": "✅ Registration successful! Please check your email."},
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
        except:
            user = None

        if user and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect("http://localhost:5173/login")
        return HttpResponse("❌ Activation link is invalid or expired.")




class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        if not check_password(password, user.password):
            return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)

        # Optional: send login email
        send_mail(
            subject="Welcome back to Bull Wheels! 🚗",
            message=f"""
Hi {user.username},

You have successfully logged in to Bull Wheels.

Enjoy exploring all the amazing wheels we have for you!

Thanks,
The Bull Wheels Team
            """,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True
        )

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        # Add admin flag
        is_admin = user.is_staff or user.is_superuser

        return Response({
            "message": "Login successful! ✅ A welcome message has been sent to your email.",
            "tokens": {
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_admin": is_admin
            }
        }, status=status.HTTP_200_OK)