from django.urls import path
from .views import AuctionBidListView, AuctionPlaceBidView

urlpatterns = [
    # List all bids for an auction
    path('auctions/<int:id>/bids/', AuctionBidListView.as_view(), name='auction-bid-list'),

    # Place a bid on an auction
    path('auctions/<int:id>/bids/place/', AuctionPlaceBidView.as_view(), name='auction-place-bid'),
]
