from rest_framework import serializers

from .models import  Rating




class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating

        fields = (
            "id",
            "user",
            "text",
            "rate",
            "product",
        )




# class ListRatingSerializer(serializers.ModelSerializer):
# #     rating_avg = serializers.IntegerField(
# #     source='product__name', 
# #     read_only=True,
# # )
#     # rating_min  = serializers.IntegerField()
#     print("we are in the ListRatingSerializer")
#     class Meta:
#         model = Rating

#         fields = (
#             # "id",
#             # "user",
#             # "text",
#             # "rate",
#             # "product",
#             "rating_avg",
#         )
 