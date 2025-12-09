

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from .models import Order
from vehicle.models import Vehicle
from .serializers import OrderSerializer, PurchaseSerializer
from users.enums import RoleChoices



# Purchase Vehicle (User Only)

class VehiclePurchaseView(generics.GenericAPIView):
    serializer_class = PurchaseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        user = request.user

        # Only USER role can buy vehicles
        if user.role != RoleChoices.USER:
            raise PermissionDenied("Only users can purchase vehicles.")

        # Pass vehicle_id to serializer
        serializer = self.get_serializer(data={'vehicle_id': id}, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        return Response({
            "message": "Vehicle purchased successfully",
            "order": OrderSerializer(order).data
        }, status=status.HTTP_201_CREATED)



# List Orders
class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        
        # Users → their own orders
        if user.role == RoleChoices.USER:
            return Order.objects.filter(user=user)
        
        # Admin & Super Admin → all orders
        return Order.objects.all()
