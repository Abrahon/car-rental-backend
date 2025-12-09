from rest_framework import serializers
from .models import Auction
from vehicle.serializers import VehicleSerializer
from users.serializers import UserSerializer
from .enums import AuctionStatus



# Auction List / Detail Serializer

class AuctionSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer(read_only=True)
    dealer = UserSerializer(read_only=True)

    class Meta:
        model = Auction
        fields = [
            'id', 'vehicle', 'dealer', 
            'start_price', 'current_price', 
            'status', 'start_time', 'end_time',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['current_price', 'status', 'created_at', 'updated_at']



# Auction Create / Update Serializer

class AuctionCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Auction
        fields = ['vehicle', 'start_price', 'start_time', 'end_time']

    def validate(self, attrs):
        user = self.context['request'].user
        vehicle = attrs.get('vehicle')

        # Only approved dealers can create auctions
        if user.role != 'DEALER' or not user.is_approved:
            raise serializers.ValidationError("Only approved dealers can create auctions.")

        # Dealer can only create auctions for their own vehicle
        if vehicle.dealer != user:
            raise serializers.ValidationError("You can only create auctions for your own vehicles.")

        # Vehicle must be available
        if vehicle.status != 'AVAILABLE':
            raise serializers.ValidationError("Vehicle must be AVAILABLE to create an auction.")

        # Start time < End time
        if attrs.get('start_time') >= attrs.get('end_time'):
            raise serializers.ValidationError("End time must be after start time.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        auction = Auction.objects.create(
            dealer=user,
            current_price=validated_data['start_price'],
            **validated_data
        )
        return auction

    def update(self, instance, validated_data):
        # Cannot update finished or cancelled auctions
        if instance.status in [AuctionStatus.FINISHED, AuctionStatus.CANCELLED]:
            raise serializers.ValidationError("Cannot update a finished or cancelled auction.")
        return super().update(instance, validated_data)
