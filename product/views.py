from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import status, authentication, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes


from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer


class LatestProductsList(APIView): 
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        products = Product.objects.all()[:4]
        serializer = ProductSerializer(products, many=True )
        return Response(serializer.data)

    # todo only authenticated user can post products
    # def post(self, request):
    #     print("we are in the serilizer")
    #     print("request.data in post", request.data)
    #     serializer = ProductSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     print(serializer.errors)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetail(APIView ):

    def get_object(self, category_slug, product_slug):
        try:
            return Product.objects.filter(category__slug=category_slug).get(slug=product_slug)
        except Product.DoesNotExist:
            raise Http404

    def get(self, request, category_slug, product_slug, format=None):
        product =  self.get_object(category_slug, product_slug) 
        serializer = ProductSerializer(product, partial=True)
        return Response(serializer.data)

class CategoryDetail(APIView):
    # def get_object(self, category_slug):
    #     try:
    #         return Category.objects.get(slug=category_slug)
    #     except Product.DoesNotExist:
    #         raise Http404

    def get(self, request, category_slug, format=None):
        # category = self.get_object(category_slug)
        
        category = get_object_or_404(Category, slug=category_slug)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

@api_view(['POST'])
def search(request):
    query =request.data.get('query', '')

    if query:
        products = Product.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    else:
        return Response({"products": []})