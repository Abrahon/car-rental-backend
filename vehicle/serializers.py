from rest_framework import serializers
from django.conf import settings
from .models import Vehicle
from .enums import VehicleStatus

User = settings.AUTH_USER_MODEL


# # -----------------------------
# # Vehicle Serializer (Public / Dealer)
# # -----------------------------
# class VehicleSerializer(serializers.ModelSerializer):
#     dealer_name = serializers.CharField(source='dealer.name', read_only=True)
#     dealer_email = serializers.CharField(source='dealer.email', read_only=True)

#     class Meta:
#         model = Vehicle
#         fields = [
#             'id', 'title', 'description', 'make', 'model', 'year',
#             'price', 'status', 'dealer', 'dealer_name', 'dealer_email',
#             'created_at', 'updated_at'
#         ]
#         read_only_fields = ['status', 'dealer', 'created_at', 'updated_at']


# # -----------------------------
# # Vehicle Create / Update Serializer (Dealer Only)
# # -----------------------------
# class VehicleCreateUpdateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Vehicle
#         fields = ['title', 'description', 'make', 'model', 'year', 'price']

#     def validate(self, attrs):
#         # Ensure dealer is approved
#         user = self.context['request'].user
#         if user.role != 'DEALER' or not user.is_approved:
#             raise serializers.ValidationError("Only approved dealers can create or update vehicles.")
#         return attrs

#     def create(self, validated_data):
#         user = self.context['request'].user
#         return Vehicle.objects.create(dealer=user, **validated_data)

#     def update(self, instance, validated_data):
#         # Prevent updating a SOLD vehicle
#         if instance.status == VehicleStatus.SOLD:
#             raise serializers.ValidationError("Cannot update a sold vehicle.")
#         return super().update(instance, validated_data)



class VehicleSerializer(serializers.ModelSerializer):
    dealer_name = serializers.ReadOnlyField(source='dealer.name')
    dealer_email = serializers.ReadOnlyField(source='dealer.email')

    class Meta:
        model = Vehicle
        fields = [
            'id', 'title', 'description', 'make', 'model', 'year',
            'price', 'status', 'dealer', 'dealer_name', 'dealer_email',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'dealer', 'created_at', 'updated_at']


class VehicleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['title', 'description', 'make', 'model', 'year', 'price']

    def validate(self, attrs):
        user = self.context['request'].user

        # Ensure dealer is approved
        if user.role != 'DEALER' or not user.is_approved:
            raise serializers.ValidationError(
                "Only approved dealers can create or update vehicles."
            )

        return attrs

    def create(self, validated_data):
        # Assign the dealer automatically
        user = self.context['request'].user
        return Vehicle.objects.create(dealer=user, **validated_data)

    def update(self, instance, validated_data):
        # Prevent updating a SOLD vehicle
        if instance.status == VehicleStatus.SOLD:
            raise serializers.ValidationError("Cannot update a sold vehicle.")

        # Prevent modifying dealer (extra protection)
        validated_data.pop('dealer', None)

        return super().update(instance, validated_data)
