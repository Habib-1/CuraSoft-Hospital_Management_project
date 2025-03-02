from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.mail import send_mail
from django.conf import settings
import jwt
from datetime import datetime, timedelta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
#for password reset
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode

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


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        email =  attrs.get("email") 
        password = attrs.get("password")
        user=User.objects.filter(email=email).first()
        if not user:
            raise serializers.ValidationError({"detail": "Incorrect email."})
        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Incorrect password."})
        if not user.is_active:
            raise serializers.ValidationError({"detail": "User is not active."})
   

        return super().validate(attrs) 

# username or email for login
# class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
#     def validate(self, attrs):
#         # Get the input from the "email" field (which can be either email or username)
#         email_or_username = attrs.get("email")
#         password = attrs.get("password")

#         # Check if the input is an email or username
#         if '@' in email_or_username:
#             user = User.objects.filter(email=email_or_username).first()
#         else:
#             user = User.objects.filter(username=email_or_username).first()

#         if not user:
#             raise serializers.ValidationError({"detail": "Incorrect email or username."})

#         if not user.check_password(password):
#             raise serializers.ValidationError({"detail": "Incorrect password."})

#         if not user.is_active:
#             raise serializers.ValidationError({"detail": "User is not active."})

#         # If everything is correct, proceed with the original validation
#         return super().validate(attrs)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name','email','gender','age','address']
        read_only_fields = ['email', 'username']

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        """Check if old password is correct"""
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        return value

    def validate_new_password(self, value):
        """Validate new password strength"""
        validate_password(value)  # Uses Django's built-in password validators
        return value

    def save(self):
        """Update user's password"""
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


# Password reset
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        """
        Check if the email exists in the database.
        """
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value

    def save(self):
        """
        Generate a password reset token and send an email to the user.
        """
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_url = f"{settings.FRONTEND_URL}/password-reset-confirm/{uid}/{token}/"  # Update with your frontend URL

        # Send email
        subject = "Password Reset Request"
        message = f"Click the link below to reset your password:\n\n{reset_url}"
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])

# Password reset confirm
class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        """
        Validate the UID, token, and new password.
        """
        try:
            uid = force_bytes(urlsafe_base64_decode(data['uid']))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid user or token.")

        if not default_token_generator.check_token(user, data['token']):
            raise serializers.ValidationError("Invalid or expired token.")

        data['user'] = user
        return data

    def save(self):
        """
        Set the new password for the user.
        """
        user = self.validated_data['user']
        user.set_password(self.validated_data['new_password'])
        user.save()