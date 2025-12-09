from django.urls import path
from .views import (
    VehicleListView,
    VehicleDetailView,
    VehicleCreateView,
    VehicleUpdateView,
    VehicleDeleteView,
    AdminVehicleListView
)

urlpatterns = [
    # Public
    path('vehicle/list/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicle/<int:id>/', VehicleDetailView.as_view(), name='vehicle-detail'),

    # Dealer (Authenticated + Approved)
    path('dealer/create/', VehicleCreateView.as_view(), name='vehicle-create'),
    path('dealer/<int:id>/update/', VehicleUpdateView.as_view(), name='vehicle-update'),
    path('dealer/<int:id>/delete/', VehicleDeleteView.as_view(), name='vehicle-delete'),
    path('api/admin/vehicles/',AdminVehicleListView.as_view(),name='vehicle-list'),
]
