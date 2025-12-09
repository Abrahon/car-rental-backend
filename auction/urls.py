from django.urls import path
from .views import AuctionCreateView, AuctionListView, AuctionDetailView,AdminAuctionListView,AdminCancelAuctionView

urlpatterns = [
    path('cars/<int:vehicle_id>/auction/create/', AuctionCreateView.as_view(),name='auction-create'),
    path('auctions/', AuctionListView.as_view(), name='auction-list'),
    path('auctions/<int:id>/', AuctionDetailView.as_view(), name='auction-detail'),
    path('admin/auctions/', AdminAuctionListView.as_view(), name='admin-auction-list'),
    path('admin/auctions/<int:id>/cancel/', AdminCancelAuctionView.as_view(), name='admin-auction-cancel'),
]
