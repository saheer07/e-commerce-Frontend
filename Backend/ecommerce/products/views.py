from django.shortcuts import render
from rest_framework import generics, viewsets
from .models import Product
from .serializers import ProductSerializer

# List + Create
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer

# Retrieve + Update + Delete
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# ViewSet (for router)
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
