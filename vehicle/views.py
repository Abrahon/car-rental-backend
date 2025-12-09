from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Vehicle
from .serializers import (
    VehicleSerializer,
    VehicleCreateUpdateSerializer,
)
from .enums import VehicleStatus
from users.enums import RoleChoices



# Public Vehicle List
# class VehicleListView(generics.ListAPIView):
#     serializer_class = VehicleSerializer
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         # Only show AVAILABLE vehicles publicly
#         return Vehicle.objects.filter(status=VehicleStatus.AVAILABLE)

from rest_framework import generics, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Vehicle
from .serializers import VehicleSerializer
from .enums import VehicleStatus

# -----------------------------
# Public Vehicle List with Search, Filter, Pagination

class VehicleListView(generics.ListAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['make', 'model', 'year', 'price']
    search_fields = ['title', 'description', 'make', 'model']
    ordering_fields = ['price', 'year', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        # Only show available vehicles where the dealer account is active
        return Vehicle.objects.filter(
            status=VehicleStatus.AVAILABLE,
            dealer__is_active=True
        )



# Public Vehicle Detail
class VehicleDetailView(generics.RetrieveAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get_queryset(self):
        queryset = Vehicle.objects.exclude(status=VehicleStatus.SOLD)
        # Public can only view AVAILABLE or SOLD
        return Vehicle.objects.exclude(status=VehicleStatus.PENDING_APPROVAL)


# Dealer Vehicle Create
class VehicleCreateView(generics.CreateAPIView):
    serializer_class = VehicleCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'DEALER' or not user.is_approved:
            raise PermissionDenied("Only approved dealers can create vehicles.")
        serializer.save()  # do NOT pass dealer=user, serializer already does it

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        vehicle = serializer.save()  # do NOT pass dealer=user

        return Response(VehicleSerializer(vehicle).data)




# Dealer Vehicle Update

class VehicleUpdateView(generics.UpdateAPIView):
    serializer_class = VehicleCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        # Dealers can only update their own approved vehicles
        if user.role == RoleChoices.DEALER and user.is_approved:
            return Vehicle.objects.filter(dealer=user)
        return Vehicle.objects.none()  # silently 404 if not allowed

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Use full VehicleSerializer for response
        full_serializer = VehicleSerializer(instance)
        return Response(full_serializer.data)




# Dealer Vehicle Delete
class VehicleDeleteView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'
    queryset = Vehicle.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.role == RoleChoices.DEALER and user.is_approved:
            return Vehicle.objects.filter(dealer=user)
        return Vehicle.objects.none()

    def perform_destroy(self, instance):
        if instance.status == VehicleStatus.SOLD:
            raise PermissionDenied("Cannot delete a sold vehicle.")
        return super().perform_destroy(instance)
    
# admin can see vehicle list
class AdminVehicleListView(generics.ListAPIView):
    serializer_class = VehicleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != RoleChoices.SUPER_ADMIN:
            raise PermissionDenied("Only Super Admin can access this.")
        return Vehicle.objects.all()
