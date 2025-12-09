
from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from django.core.validators import RegexValidator


User = get_user_model() 


# ---------------------------
# SIGNUP SERIALIZER
# ---------------------------
from rest_framework import serializers
from django.core.validators import RegexValidator
from django.contrib.auth import get_user_model

User = get_user_model()  # your custom User model

# class SignupSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(
#         write_only=True,
#         min_length=8,
#         error_messages={
#             "min_length": "Password must be at least 8 characters long.",
#             "blank": "Password field cannot be empty.",
#         },
#     )
#     confirm_password = serializers.CharField(
#         write_only=True,
#         min_length=8,
#         error_messages={
#             "min_length": "Confirm password must be at least 8 characters long.",
#             "blank": "Confirm password field cannot be empty.",
#         },
#     )

#     name = serializers.CharField(
#         validators=[
#             RegexValidator(
#                 regex=r"^[A-Za-z\s]+$",
#                 message="Name can only contain letters and spaces.",
#             )
#         ],
#         error_messages={
#             "blank": "Name field is required.",
#             "required": "Please provide your name.",
#         },
#     )

#     class Meta:
#         model = User
#         fields = ["name", "email", "password", "confirm_password", "role"]

#     def validate_email(self, value):
#         if User.objects.filter(email=value).exists():
#             raise serializers.ValidationError("This email is already registered.")
#         return value

#     def validate(self, attrs):
#         if attrs.get("password") != attrs.get("confirm_password"):
#             raise serializers.ValidationError(
#                 {"confirm_password": "Passwords do not match."}
#             )
#         return attrs

class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "min_length": "Password must be at least 8 characters long.",
            "blank": "Password field cannot be empty.",
        },
    )
    confirm_password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={
            "min_length": "Confirm password must be at least 8 characters long.",
            "blank": "Confirm password field cannot be empty.",
        },
    )

    name = serializers.CharField(
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z\s]+$",
                message="Name can only contain letters and spaces.",
            )
        ],
        error_messages={
            "blank": "Name field is required.",
            "required": "Please provide your name.",
        },
    )

    class Meta:
        model = User
        fields = ["name", "email", "password", "confirm_password", "role"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already registered.")
        return value

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("confirm_password"):
            raise serializers.ValidationError(
                {"confirm_password": "Passwords do not match."}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(**validated_data)
        return user

# ---------------------------
# LOGIN SERIALIZER
# ---------------------------
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError("Invalid email or password.")
        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")
        attrs["user"] = user
        return attrs





class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'is_active', 'is_approved', 'date_joined']



# -----------------------------
# Dealer Approval Serializer
# -----------------------------
# serializers.py
class DealerApprovalSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'role', 'is_approved', 'is_active']

