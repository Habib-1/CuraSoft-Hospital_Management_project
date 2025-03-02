from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.backends import ModelBackend

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'gender', 'age', 'address', 'password', 'password2']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match"})
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            gender=validated_data['gender'],
            age=validated_data['age'],
            address=validated_data['address'],
        )
        user.set_password(validated_data['password'])
        user.save() 

        # Generate JWT token for email verification
        token = jwt.encode(
            {"user_id": user.id, "exp": datetime.utcnow() + timedelta(hours=24)},
            settings.SECRET_KEY,
            algorithm="HS256"
        )
        # Send verification email to user
        verification_link = f"http://127.0.0.1:8000/verify-email/?token={token}"
        send_mail(
            subject="Verify Your Email",
            message=f"Click the link to verify your account: {verification_link}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )

        return user


# Custom serializer for login with email/username and if is_active is True

# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     username_field = "username_or_email"

#     def validate(self, attrs):
#         username_or_email = attrs.get("username_or_email")
#         password = attrs.get("password")

#         # Check if user exists
#         user = None
#         if User.objects.filter(email=username_or_email).exists():
#             user = User.objects.get(email=username_or_email)
#         elif User.objects.filter(username=username_or_email).exists():
#             user = User.objects.get(username=username_or_email)

#         if not user:
#             raise serializers.ValidationError({"error": "No active account found with the given credentials(Username)"})

#         # Check if password is correct
#         if not user.check_password(password):
#             raise serializers.ValidationError({"error": "No active account found with the given credentials(Password)"})

#         # Check if account is verified
#         if not user.is_active:
#             raise serializers.ValidationError({"error": "Account is not verified!"})

#         # Generate token
#         data = super().validate(attrs)
#         data['username'] = user.username
#         data['email'] = user.email
#         return data

class EmailOrUsernameAuthBackend(ModelBackend):
    """Custom authentication backend to allow login using email or username"""
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(email=username).first() or User.objects.filter(username=username).first()
        if user and user.check_password(password):
            return user
        return None

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_or_email = attrs.get("username")  # SimpleJWT expects 'username' field
        password = attrs.get("password")

        # Check if user exists
        user = User.objects.filter(email=username_or_email).first() or User.objects.filter(username=username_or_email).first()
        if not user:
            raise serializers.ValidationError({"error": "No active account found with the given credentials (Username or Email)"})

        # Check if account is active
        if not user.is_active:
            raise serializers.ValidationError({"error": "Your account is inactive. Please contact support."})

        # Authenticate user using custom backend
        user = authenticate(request=self.context.get('request'), username=username_or_email, password=password)
        if not user:
            raise serializers.ValidationError({"error": "No active account found with the given credentials (Password)"})

        # Generate token
        refresh = self.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "username": user.username,
            "email": user.email,
        }
