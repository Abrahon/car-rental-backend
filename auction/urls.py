from django.urls import path
from .views import AuctionCreateView, AuctionListView, AuctionDetailView

urlpatterns = [
    path('cars/<int:vehicle_id>/auction/', AuctionCreateView.as_view(), name='auction-create'),
    path('auctions/', AuctionListView.as_view(), name='auction-list'),
    path('auctions/<int:id>/', AuctionDetailView.as_view(), name='auction-detail'),
]
