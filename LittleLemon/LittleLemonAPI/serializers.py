from .models import *
from rest_framework import serializers
from django.contrib.auth.models import User
from decimal import Decimal

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        category = CategorySerializer(read_only=True)
        fields = ['id', 'title', 'price', 'featured', 'category']
        extra_kwargs = {
            'price': {'min_value': 0.99}
        }

class MenuItemSerializer2(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title', 'price']
        extra_kwargs = {
            'price': {'min_value': 0.99}
        }

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        user = UserSerializer(read_only=True)
        menuitem = MenuItemSerializer(read_only=True)
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'quantity': {"min_value": 1}
        }

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        user = UserSerializer(read_only=True)
        fields = ['user', 'delivery_crew', 'status', 'total', 'date']

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        user = UserSerializer(read_only=True)
        menuitem = MenuItemSerializer(read_only=True)
        fields = ['user', 'menuitem', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'quantity': {"min_value": 1}
        }