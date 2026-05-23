from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    category_details = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'image', 'price', 'stock', 'is_active',
            'category', 'category_details', 'created_at', 'updated_at',
        ]
        read_only_fields = ['category_details', 'created_at', 'updated_at']

    def validate_name(self, value):
        if len(value) < 3 or len(value) > 255:
            raise serializers.ValidationError("Product name must be between 3 and 255 characters.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock must be at least 0.")
        return value