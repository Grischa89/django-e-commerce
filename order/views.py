import stripe

from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Order, OrderItem
from .serializers import OrderSerializer, MyOrderSerializer

# def test_func(a,b):
#     return a + b

@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def checkout(request):
    # print("checkout request:", request)
    # print("checkout request.data:", request.data)
    # print("len(request-data):", request.data.items)
    serializer = OrderSerializer(data=request.data)
    # print("checkout serializer:", serializer)
    
    if serializer.is_valid():
        # print("serializer.validated_data['items']: ", serializer.validated_data['items'])
        stripe.api_key = settings.STRIPE_SECRET_KEY
        paid_amount = sum(item.get('quantity') * item.get('product').price for item in serializer.validated_data['items'])

        try:
            charge = stripe.Charge.create(
                amount=int(paid_amount * 100),
                currency='USD',
                description='Charge from Djackets',
                source=serializer.validated_data['stripe_token']
            )
            serializer.save(user=request.user, paid_amount=paid_amount)
            return Response("Success", status=status.HTTP_201_CREATED)
        except Exception as e:
            print((str(e)))
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #print("serializer.errors: ", serializer.errors, serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class OrdersList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        orders = Order.objects.filter(user = request.user)
        serializer = MyOrderSerializer(orders, many=True)
        return Response(serializer.data)