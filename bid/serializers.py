from rest_framework import serializers
from .models import Bid, Auction
from users.enums import RoleChoices
from vehicle.enums import VehicleStatus
from django.utils import timezone


class BidSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    auction_id = serializers.IntegerField(source='auction.id', read_only=True)

    class Meta:
        model = Bid
        fields = ['id', 'auction', 'auction_id', 'user', 'user_name', 'user_email', 'amount', 'created_at']
        read_only_fields = ['id', 'user', 'created_at', 'auction_id', 'user_name', 'user_email']



# Place a Bid Serializer

# class PlaceBidSerializer(serializers.Serializer):
#     auction_id = serializers.IntegerField()
#     amount = serializers.DecimalField(max_digits=12, decimal_places=2)

#     def validate_auction_id(self, value):
#         try:
#             auction = Auction.objects.get(id=value)
#         except Auction.DoesNotExist:
#             raise serializers.ValidationError("Auction does not exist.")

#         self.context['auction'] = auction
#         return value

#     def validate(self, attrs):
#         auction = self.context['auction']
#         user = self.context['request'].user
#         bid_amount = attrs.get('amount')

#         # Rule: Only USER role can bid
#         if user.role != RoleChoices.USER:
#             raise serializers.ValidationError("Only users can place bids.")

#         # Rule: Auction must be ACTIVE
#         now = timezone.now()
#         if not (auction.status == 'ACTIVE' and auction.start_time <= now <= auction.end_time):
#             raise serializers.ValidationError("Auction is not active.")

#         # Rule: Dealer cannot bid on own auction
#         if auction.dealer == user:
#             raise serializers.ValidationError("Dealers cannot bid on their own auctions.")

#         # Rule: Bid must be greater than highest bid or start price
#         highest_bid = auction.bids.order_by('-amount').first()
#         min_bid = highest_bid.amount if highest_bid else auction.start_price
#         if bid_amount <= min_bid:
#             raise serializers.ValidationError(f"Bid must be greater than current highest bid ({min_bid}).")

#         return attrs

#     def create(self, validated_data):
#         user = self.context['request'].user
#         auction = self.context['auction']
#         bid_amount = validated_data['amount']

#         bid = Bid.objects.create(
#             auction=auction,
#             user=user,
#             amount=bid_amount
#         )
#         # Optionally update auction.current_price
#         auction.current_price = bid_amount
#         auction.save(update_fields=['current_price'])
#         return bid
from rest_framework import serializers
from django.utils import timezone
from .models import Auction, Bid
from users.enums import RoleChoices
from auction .enums import AuctionStatus


class PlaceBidSerializer(serializers.Serializer):
    auction_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)

    def validate_auction_id(self, value):
        try:
            auction = Auction.objects.get(id=value)
        except Auction.DoesNotExist:
            raise serializers.ValidationError("Auction does not exist.")

        self.context['auction'] = auction
        return value

    def validate(self, attrs):
        auction = self.context['auction']
        user = self.context['request'].user
        bid_amount = attrs.get('amount')

        # -----------------------------
        # Update auction status dynamically
        # -----------------------------
        now = timezone.now()
        if auction.start_time <= now <= auction.end_time:
            auction.status = AuctionStatus.ACTIVE
            auction.save(update_fields=['status'])
        elif now > auction.end_time:
            auction.status = AuctionStatus.FINISHED
            auction.save(update_fields=['status'])


        # Rule: Only USER role can bid
        if user.role != RoleChoices.USER:
            raise serializers.ValidationError("Only users can place bids.")

        # Rule: Auction must be ACTIVE
        if auction.status != AuctionStatus.ACTIVE:
            raise serializers.ValidationError("Auction is not active.")

        # Rule: Dealer cannot bid on own auction
        if auction.dealer == user:
            raise serializers.ValidationError("Dealers cannot bid on their own auctions.")

        # Rule: Bid must be greater than highest bid or start price
        highest_bid = auction.bids.order_by('-amount').first()
        min_bid = highest_bid.amount if highest_bid else auction.start_price
        if bid_amount <= min_bid:
            raise serializers.ValidationError(
                f"Bid must be greater than current highest bid ({min_bid})."
            )

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        auction = self.context['auction']
        bid_amount = validated_data['amount']

        bid = Bid.objects.create(
            auction=auction,
            user=user,
            amount=bid_amount
        )

        # Update auction current price
        auction.current_price = bid_amount
        auction.save(update_fields=['current_price'])

        return bid
