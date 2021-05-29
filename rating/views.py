from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from rest_framework import status, authentication, permissions
from rest_framework.decorators import authentication_classes, permission_classes
from .serializers import RatingSerializer
from . models import Rating

from rest_framework.views import APIView

from product.models import Product
from rating.models import Rating
from .serializers import RatingSerializer
from django.db.models import Min, Max, Avg, F
from django.shortcuts import get_object_or_404

# @api_view(['GET'])
# @authentication_classes([authentication.TokenAuthentication])
# @permission_classes([permissions.IsAuthenticated])


class FullRatingsList(APIView):

    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product = self.get_object(category_slug, product_slug)
        ratings = Rating.objects.filter( product=product.id )
        serializer = RatingSerializer(ratings, many=True )

        return Response(serializer.data)

class RatingsViewSet(APIView):

    def get(self, request):
        rating_avg =  Rating.objects.values('product__id').annotate(Max('rate'))
        # print("annotate: ",rating_avg, type(rating_avg))
        # print("after init", dir(rating_avg))
        # print("rating_avg[0]: ", rating_avg[0])
        # print("rating_avg[1]: ", dir(rating_avg[0]))
        # print("rating_avg[0]: ", rating_avg[0].items)
        product = get_object_or_404(
                Product.objects.annotate(avg_score=Avg('rating__rate')),
                pk=1
            )
        # print("product::: ", product, Product.objects.all())
        queryset1 = Product.objects.filter(
        name__startswith='F')
        
        # print("queryset1: ",queryset1)
        # print(queryset1)
        # print(dir(queryset1))
        # print(queryset1.all())
        # print(queryset1.values())
        # print(queryset1.values_list())
        
        # if serializer.is_valid():
            # print("serializer.errors: ", serializer.errors)
        return Response(rating_avg, status=status.HTTP_201_CREATED)
        # print("serializer.errors: ", serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def rate_product(request, category_slug, product_slug):
    # print("in the rate_product:", request.data, request.user.id)
    # if "product" not in request.data:
    #     print("haha")
    #     return Response("There is no product in there")
    # if request.user.id == 11:
    #     print(request.user.id)
    #     print("There is not user id in the request")
    #     return Response("There is not user id in the request")
    request.data['user'] = request.user.id
    serializer = RatingSerializer(data=request.data)
    # print("serializer: ", serializer)

    if serializer.is_valid():

        serializer.save()

        ratings = Rating.objects.filter(product=request.data['product'])
        Product.objects.filter(id=request.data['product']).update(counter_rating=ratings.count())
        #use this when more products/ratings
        # Product.objects.filter(id=request.data['product']).update(counter_rating=F('counter_rating') + 1)
        average_rating = Rating.objects.filter( product=request.data['product'] ).aggregate(Avg('rate'))
        Product.objects.filter(id=request.data['product']).update(average_rating=average_rating['rate__avg'])

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    print(serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)