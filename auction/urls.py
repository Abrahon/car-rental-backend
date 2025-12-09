from django.urls import path
from .views import AuctionCreateView, AuctionListView, AuctionDetailView,AdminAuctionListView

urlpatterns = [
    path('cars/<int:vehicle_id>/auction/', AuctionCreateView.as_view(), name='auction-create'),
    path('auctions/', AuctionListView.as_view(), name='auction-list'),
    path('auctions/<int:id>/', AuctionDetailView.as_view(), name='auction-detail'),
    path('api/auction/list/',AdminAuctionListView.as_view(),name='auction-list')

]
