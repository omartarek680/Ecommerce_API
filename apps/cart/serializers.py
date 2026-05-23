from rest_framework import serializers
from .models import CartItem, Product, Cart
from apps.products.serializers import ProductSerializer




class CartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.PrimaryKeyRelatedField(source='product', queryset=Product.objects.all(), write_only=True)
    product_details = ProductSerializer(source='product', read_only=True)
    total_subprice = serializers.ReadOnlyField()
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'product_details', 'total_subprice', 'quantity']

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

  
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']
    