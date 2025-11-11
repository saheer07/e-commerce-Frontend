from rest_framework import serializers
from .models import Product
from reviews.serializers import ReviewSerializer  # import review serializer

class ProductSerializer(serializers.ModelSerializer):
    # Include all related reviews for this product
    product_reviews = ReviewSerializer(many=True, read_only=True)
    
    # Computed fields
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'brand',          # 🆕 added
            'color',          # 🆕 added
            'description',
            'price',
            'category',
            'image',
            'rating',
            'stock',
            'created_at',
            'average_rating',
            'review_count',
            'product_reviews'
        ]

    def get_average_rating(self, obj):
        """Calculate average rating from all product reviews"""
        reviews = obj.product_reviews.all()
        if reviews.exists():
            return round(sum(r.rating for r in reviews) / reviews.count(), 1)
        return 0.0

    def get_review_count(self, obj):
        """Count total reviews"""
        return obj.product_reviews.count()
