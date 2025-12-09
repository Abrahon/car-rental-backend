from django.urls import path, include
from .views import (
    SignupView, 
    LoginView,
    DealerApprovalView,
    DealerListView

)
urlpatterns = [
    # Your custom authentication views
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/admin/dealers/<int:id>/approve/', DealerApprovalView.as_view(), name='admin-dealer-approve'),
    path('auth/admin/dealers/', DealerListView.as_view(), name='admin-dealer-list'),
 
]