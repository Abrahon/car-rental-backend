from django.urls import path
from .views import VehiclePurchaseView, OrderListView

urlpatterns = [
    # Purchase a vehicle
    path('purchase/<int:id>/', VehiclePurchaseView.as_view(), name='vehicle-purchase'),

    # List orders (user → own orders, admin → all orders)
    path('orders/', OrderListView.as_view(), name='order-list'),
]
