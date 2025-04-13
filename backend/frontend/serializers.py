from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Fabric, Garment, Order, Product

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

class FabricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fabric
        fields = '__all__'

class GarmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garment
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    fabric = FabricSerializer(many = True)

    class Meta:
        model = Product
        fields = '__all__'
