from django.urls import path
from .views import RegisterView, LoginView, ActivateAccountView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', ActivateAccountView.as_view(), name='activate'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
