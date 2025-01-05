from .models import User
from django.contrib.auth import authenticate
from django.utils.encoding import force_str
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .tasks import send_password_reset_link
from .serializers import (
    UserSerializer,
    EmailVerificationSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    SetNewPasswordSerializer,
)

# Create your views here.


class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            return Response(
                {
                    "user": self.serializer_class(user).data,
                },
                status=status.HTTP_201_CREATED,
            )

        print("Serializer Errors", serializer.errors)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class EmailConfirmationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = EmailVerificationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        uid = serializer.validated_data["uid"]

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
            user.is_active = True
            user.is_verified = True
            user.save()

            return Response(
                {"message": "Email successfully verified"},
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"message": "Invalid link or user does not exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                email=serializer.validated_data.get("email"),
                password=serializer.validated_data.get("password"),
            )

            if user:
                if not user.is_verified:
                    return Response(
                        {
                            "message": "Email is not verified",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                token, created = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "user": LoginSerializer(user).data,
                        "token": token.key,
                    }
                )

        print("Authentication failed")
        return Response(
            {"message": "Invalid credentials"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        try:
            if serializer.is_valid(raise_exception=True):
                email = serializer.validated_data["email"]
                send_password_reset_link.delay(email)
                return Response(
                    {"message": "Password reset email sent successfully."},
                    status=status.HTTP_200_OK,
                )

        except ValidationError as e:
            print(f"Error sending email: {str(e)}")
            return Response(
                {"message": "Email address is not registered"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class SetNewPasswordView(APIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data["password"]
            uidb64 = serializer.validated_data["uid"]
            token = serializer.validated_data["token"]

            try:
                user_id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=user_id)
            except User.DoesNotExist:
                raise AuthenticationFailed(detail="Invalid reset link")
            except ValueError:
                raise AuthenticationFailed(detail="Invalid reset link")

            if not default_token_generator.check_token(user, token):
                raise AuthenticationFailed(
                    detail="Reset link is invalid or has expired",
                )

            user.set_password(password)
            user.save()

            return Response(
                {
                    "success": True,
                    "message": "Password reset successful",
                },
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )
