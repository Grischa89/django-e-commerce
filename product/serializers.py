from rest_framework import serializers

from .models import Category, Product

class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "get_absolute_url",
            "description",
            "price",
            "get_image",
            "get_thumbnail",
            "average_rating",
            "counter_rating",

        )

class CategorySerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    # average_rating  = serializers.IntegerField()
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
            "get_absolute_url",
            "products",
            
        )
