from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductListCreateView, ProductDetailView, ProductViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('api/', include(router.urls)),  # router-based CRUD
    path('products/', ProductListCreateView.as_view(), name='product-list'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]
