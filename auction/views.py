from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from django.shortcuts import get_object_or_404

from .models import Auction
from vehicle.models import Vehicle
from .serializers import AuctionSerializer, AuctionCreateUpdateSerializer
from .enums import AuctionStatus
from users.enums import RoleChoices


# Create Auction (Dealer Only)
class AuctionCreateView(generics.CreateAPIView):
    serializer_class = AuctionCreateUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, vehicle_id, *args, **kwargs):
        user = request.user

        # Only approved dealers
        if user.role != RoleChoices.DEALER or not user.is_approved:
            raise PermissionDenied("Only approved dealers can create auctions.")

        # Fetch vehicle
        vehicle = get_object_or_404(Vehicle, id=vehicle_id)

        # Vehicle must be AVAILABLE and not in another active auction
        if vehicle.status != 'AVAILABLE':
            raise ValidationError("Vehicle must be AVAILABLE to create an auction.")
        if Auction.objects.filter(vehicle=vehicle, status__in=[AuctionStatus.SCHEDULED, AuctionStatus.ACTIVE]).exists():
            raise ValidationError("This vehicle already has an ongoing auction.")

        serializer = self.get_serializer(
            data={
                'vehicle': vehicle.id,
                'start_price': request.data.get('start_price'),
                'start_time': request.data.get('start_time'),
                'end_time': request.data.get('end_time')
            },
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        auction = serializer.save()

        return Response({
            "message": "Auction created successfully",
            "auction": AuctionSerializer(auction).data
        }, status=status.HTTP_201_CREATED)



# List All Auctions (Public)
class AuctionListView(generics.ListAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        # Update auction status dynamically
        now = timezone.now()
        for auction in Auction.objects.filter(status__in=[AuctionStatus.SCHEDULED, AuctionStatus.ACTIVE]):
            if auction.end_time <= now:
                auction.status = AuctionStatus.FINISHED
                auction.save()
            elif auction.start_time <= now <= auction.end_time:
                auction.status = AuctionStatus.ACTIVE
                auction.save()

        return Auction.objects.all()



# Auction Detail (Public)
class AuctionDetailView(generics.RetrieveAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

    def get_queryset(self):
        # Update auction status dynamically
        now = timezone.now()
        for auction in Auction.objects.filter(status__in=[AuctionStatus.SCHEDULED, AuctionStatus.ACTIVE]):
            if auction.end_time <= now:
                auction.status = AuctionStatus.FINISHED
                auction.save()
            elif auction.start_time <= now <= auction.end_time:
                auction.status = AuctionStatus.ACTIVE
                auction.save()

        return Auction.objects.all()


# admin
class AdminAuctionListView(generics.ListAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != RoleChoices.SUPER_ADMIN:
            raise PermissionDenied("Only Super Admin can access this.")
        return Auction.objects.all()


    

# Cancel an auction (Super Admin Only)
class AdminCancelAuctionView(generics.UpdateAPIView):
    serializer_class = AuctionSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Auction.objects.all()
    lookup_field = 'id'

    def patch(self, request, *args, **kwargs):
        user = request.user
        if user.role != RoleChoices.SUPER_ADMIN:
            raise PermissionDenied("Only Super Admin can cancel auctions.")

        auction = self.get_object()
        auction.status = 'CANCELLED'
        auction.save()
        return Response({"message": "Auction cancelled successfully.", "auction": AuctionSerializer(auction).data})
