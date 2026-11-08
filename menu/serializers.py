from rest_framework import serializers
from .models import Category, Dish


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ['id', 'name', 'description', 'price', 'category', 'is_available']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError('Ціна має бути більшою за 0.')
        return value
