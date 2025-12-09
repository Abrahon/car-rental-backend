from django.urls import path
from .views import AuctionBidListView, AuctionPlaceBidView,AdminBidListView

urlpatterns = [
    path('auctions/<int:id>/bids/', AuctionBidListView.as_view(), name='auction-bid-list'),

    path('auctions/<int:id>/bids/place/', AuctionPlaceBidView.as_view(), name='auction-place-bid'),
    path('admin/bids/', AdminBidListView.as_view(), name='admin-bid-list'),
]
