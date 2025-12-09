from django.urls import path, include
from .views import (
    SignupView, 
    LoginView,
    DealerApprovalView

)
urlpatterns = [
    # Your custom authentication views
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/admin/dealers/<int:pk>/approve/', DealerApprovalView.as_view(), name='dealer-approve'),
 
]