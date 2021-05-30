from rest_framework import serializers

from .models import Category, Product, WeAreTheWorld

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
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

# class ProductRatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WeAreTheWorld


#         fields = (
#             # "id",
#             "user_id",
#             "text",
#             "rate",
#             # "product",
#         )
