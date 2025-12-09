from rest_framework import serializers
from django.conf import settings
from .models import Vehicle, Order
from vehicle.enums import VehicleStatus

User = settings.AUTH_USER_MODEL



# -----------------------------
# Order Serializer (Read-Only)
# -----------------------------
class OrderSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    vehicle_title = serializers.CharField(source='vehicle.title', read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'user_name', 'user_email', 'vehicle', 'vehicle_title', 'price', 'created_at']
        read_only_fields = ['id', 'user', 'vehicle', 'price', 'created_at']


# -----------------------------
# Purchase Serializer (User buys vehicle)
# -----------------------------
class PurchaseSerializer(serializers.Serializer):
    vehicle_id = serializers.IntegerField()

    def validate_vehicle_id(self, value):
        try:
            vehicle = Vehicle.objects.get(id=value)
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError("Vehicle does not exist.")

        if vehicle.status != VehicleStatus.AVAILABLE:
            raise serializers.ValidationError("Vehicle is not available for purchase.")

        self.context['vehicle'] = vehicle
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        vehicle = self.context['vehicle']

        # Create order
        order = Order.objects.create(
            user=user,
            vehicle=vehicle,
            price=vehicle.price
        )

        # Mark vehicle as SOLD
        vehicle.status = VehicleStatus.SOLD
        vehicle.save()

        return order
