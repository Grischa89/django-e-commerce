from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from stripe.six import assertCountEqual
from .factories import  OrderFactory, OrderItemFactory
from order.models import Order, OrderItem
from order.views import checkout
from product.tests.factories import ProductFactory, CategoryFactory
from rest_framework.test import APIClient
from unittest import mock

CHECKOUT_URL = reverse('checkout')

class PrivateOrderModelTest(TestCase):
    """Test the order model"""

    def setUp(self):
        self.client = APIClient()
        self.user = self.client.post('/api/v1/users/', data={
                                    'username':'jana',
                                    'password':'1-keep-c0ding'
                                    })
        res = self.client.post('/api/v1/token/login/', data={
                                    'username':'jana',
                                    'password':'1-keep-c0ding'})

        self.token=res.data['auth_token']
        self.api_authentication()
        User = get_user_model()
        user = User.objects.get(username='jana')
        self.category_summer = CategoryFactory(name="summer")
        self.product = ProductFactory(category=self.category_summer,
                                      name="Sample product")
        self.product1 = ProductFactory(category=self.category_summer,
                                      name="Sample product 1")
        
        self.order1 = OrderFactory(user=user, orderitems=[self.product, self.product1])
        # self.create_order()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_order___str__(self):
        """test order return value"""
        self.assertEqual(self.order1.__str__(), self.order1.first_name)

    def test_orderitem___str__(self):
        """test orderitem return value"""
        order_item = OrderItem.objects.first()
        self.assertEqual(order_item.__str__(), str(order_item.id))
