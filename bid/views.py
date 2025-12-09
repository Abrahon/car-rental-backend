from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from .models import Auction, Bid
from .serializers import BidSerializer, PlaceBidSerializer
from users.enums import RoleChoices
from django.utils import timezone



# List all bids for an auction
class AuctionBidListView(generics.ListAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        auction_id = self.kwargs['id']
        auction = get_object_or_404(Auction, id=auction_id)
        return auction.bids.all().order_by('-amount')



# Place a bid on an auction
# class AuctionPlaceBidView(generics.GenericAPIView):
#     serializer_class = PlaceBidSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def post(self, request, id, *args, **kwargs):
#         serializer = self.get_serializer(data={'auction_id': id, **request.data}, context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         bid = serializer.save()
#         return Response({
#             "message": "Bid placed successfully",
#             "bid": BidSerializer(bid).data
#         }, status=status.HTTP_201_CREATED)
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .serializers import PlaceBidSerializer
from .models import Bid

class AuctionPlaceBidView(generics.GenericAPIView):
    serializer_class = PlaceBidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, id, *args, **kwargs):
        # Pass auction_id to serializer along with request data
        serializer = self.get_serializer(
            data={'auction_id': id, **request.data},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        bid = serializer.save()
        return Response({
            "message": "Bid placed successfully",
            "bid": {
                "id": bid.id,
                "auction": bid.auction.id,
                "user": bid.user.id,
                "amount": str(bid.amount),
                "created_at": bid.created_at
            }
        }, status=status.HTTP_201_CREATED)


# List all bids (Super Admin Only)
class AdminBidListView(generics.ListAPIView):
    serializer_class = BidSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role != RoleChoices.SUPER_ADMIN:
            raise PermissionDenied("Only Super Admin can access bids.")
        return Bid.objects.all()
