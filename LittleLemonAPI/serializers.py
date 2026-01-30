from rest_framework import serializers
from .models import MenuItem, Cart, Order, OrderItem
from django.contrib.auth.models import User
from rest_framework.validators import UniqueTogetherValidator

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = '__all__'
        extra_kwargs = {
            'price' : {'min_value' : 5}
        }

class CartSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault()) #user does NOT appear in: Request/Response body
    unit_price = serializers.ReadOnlyField()
    price = serializers.ReadOnlyField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price']
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Cart.objects.all(),
                fields=['user', 'menuitem']
            )
        ]

    def create(self, validated_data):
        menuitem = validated_data['menuitem']
        quantity = validated_data['quantity']

        unit_price = menuitem.price
        total_price = unit_price * quantity

        validated_data['unit_price'] = unit_price
        validated_data['price'] = total_price

        return super().create(validated_data)


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
