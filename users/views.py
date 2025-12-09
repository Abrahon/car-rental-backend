# users/views.py

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser,IsAuthenticated
# from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.exceptions import PermissionDenied



from .serializers import SignupSerializer, LoginSerializer, DealerApprovalSerializer,UserSerializer

from .enums import RoleChoices
User = get_user_model()


# -----------------------------
# Helper: Generate JWT tokens
# -----------------------------
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    # Optional extra info in token payload
    refresh['role'] = user.role
    refresh['name'] = user.name
    refresh['email'] = user.email
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


# -----------------------------
# User Signup (Register)
# -----------------------------
class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        message = "User created successfully"
        if user.role == 'DEALER' and not user.is_approved:
            message = "Dealer account created. Awaiting admin approval."

        return Response({
            "message": message,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
                "is_approved": getattr(user, 'is_approved', None),
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # -----------------------------
        # Dealer approval check
        # -----------------------------
        if user.role == "DEALER" and not user.is_approved:
            return Response(
                {"message": "Dealer account not approved yet."},
                status=status.HTTP_403_FORBIDDEN
            )

        # -----------------------------
        # Generate tokens
        # -----------------------------
        tokens = get_tokens_for_user(user)

        return Response({
            "message": "Login successful",
            "token": tokens,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "role": user.role,
            }
        }, status=status.HTTP_200_OK)




# Dealer Approval (Super Admin Only)

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import get_user_model
from .serializers import DealerApprovalSerializer
from .enums import RoleChoices

User = get_user_model()


class DealerApprovalView(generics.UpdateAPIView):
    queryset = User.objects.filter(role=RoleChoices.DEALER)
    serializer_class = DealerApprovalSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "id"  # Must match URL parameter

    def patch(self, request, *args, **kwargs):
        dealer = self.get_object()
        action = request.data.get("action")  # "approve" or "deny"

        if action == "approve":
            dealer.is_approved = True
            dealer.is_active = True  # Optional: allow login after approval
            message = "Dealer approved successfully"
        elif action == "deny":
            dealer.is_approved = False
            dealer.is_active = False  # Optional: disable login
            message = "Dealer denied successfully"
        else:
            return Response(
                {"error": "Invalid action. Use 'approve' or 'deny'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        dealer.save()
        serializer = self.get_serializer(dealer)

        return Response({
            "status": message,
            "dealer": serializer.data
        }, status=status.HTTP_200_OK)


class DealerListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != RoleChoices.SUPER_ADMIN:
            raise PermissionDenied("Only Super Admin can access this.")
        return User.objects.filter(role=RoleChoices.DEALER)
