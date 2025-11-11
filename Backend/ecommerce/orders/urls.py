from django.urls import path
from .views import (
    CreateOrderAPIView,
    RazorpayOrderCreateAPIView,
    RazorpayVerifyAPIView,
    OrderAPIView,
)

urlpatterns = [
    path("create/", CreateOrderAPIView.as_view(), name="create-order"),
    path("razorpay/create/", RazorpayOrderCreateAPIView.as_view(), name="razorpay-order"),
    path("razorpay/verify/", RazorpayVerifyAPIView.as_view(), name="razorpay-verify"),
    path("", OrderAPIView.as_view(), name="orders"),
]
