from rest_framework import serializers
from .models import Category, Product, ProductImage, ProductVariant, Review

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description', 'image', 'parent', 'subcategories', 'created_at')
    
    def get_subcategories(self, obj):
        if obj.subcategories.exists():
            return CategorySerializer(obj.subcategories.all(), many=True).data
        return []

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('id', 'image', 'is_primary', 'alt_text')

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('id', 'name', 'value', 'price_adjustment', 'stock', 'sku')

class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.ReadOnlyField(source='user.email')
    
    class Meta:
        model = Review
        fields = ('id', 'user', 'user_email', 'rating', 'title', 'comment', 'created_at')
        read_only_fields = ('user',)

class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    category_name = serializers.ReadOnlyField(source='category.name')
    reviews_count = serializers.SerializerMethodField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    
    class Meta:
        model = Product
        fields = ('id', 'name', 'slug', 'description', 'short_description', 'price', 
                  'compare_price', 'category', 'category_name', 'stock', 'sku', 
                  'is_active', 'is_featured', 'average_rating', 'total_reviews',
                  'images', 'variants', 'reviews_count', 'created_at', 'updated_at')
    
    def get_reviews_count(self, obj):
        return obj.reviews.count()