# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from django.urls import reverse
# from stripe.six import assertCountEqual
# from .factories import  OrderFactory
# from order.views import checkout
# from order.models import OrderItem, Order
# from product.tests.factories import ProductFactory, CategoryFactory
# from rest_framework.test import APIClient
# from unittest import mock

# CHECKOUT_URL = reverse('checkout')

# class PrivateOrderModelTest(TestCase):
#     """Test the product model"""

#     def setUp(self):
#         self.client = APIClient()
#         self.user = self.client.post('/api/v1/users/', data={
#                                     'username':'jana',
#                                     'password':'1-keep-c0ding'
#                                     })
#         res = self.client.post('/api/v1/token/login/', data={
#                                     'username':'jana',
#                                     'password':'1-keep-c0ding'})

#         self.token=res.data['auth_token']
#         self.api_authentication()
#         User = get_user_model()
#         user = User.objects.get(username='jana')
#         self.category_summer = CategoryFactory(name="summer")
#         self.product = ProductFactory(category=self.category_summer,
#                                       name="Sample product", price=50.49)
#         self.product1 = ProductFactory(category=self.category_summer,
#                                       name="Sample product 1", price=149.51)
  
#         self.order1 = OrderFactory(user=user, 
#                         orderitems=[self.product, self.product1])

#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)


#     # def test_orderitem(self):
#     #     order_item = OrderItem.objects.first()
#     #     print(order_item.product_id, order_item.product,
#     #           order_item.price)
#     #     order = Order.objects.last()
#     #     print(order.paid_amount, order.user)
#     @mock.patch("order.views.stripe.Charge.create")
#     def test_order___str__(self, mock_event_create):
#         """ test checkout success """
#         mock_event_create.return_value = "WE THE BEST MUSIC"
        
#         params = {'first_name': self.order1.first_name,
#                  'last_name': self.order1.last_name, 
#                  'email': self.order1.email,
#                  'address': self.order1.address,
#                  'zipcode': self.order1.zipcode,
#                  'place': self.order1.place,
#                  'phone': self.order1.phone,
#                  'items': [{
#                  'product': self.product1.id,
#                  'quantity': 1,
#                  'price': self.product1.price
#                  },
#                  {'product': self.product.id,
#                  'quantity': 1,
#                  'price':self.product.price}
#                  ],
#                  'stripe_token': self.order1.stripe_token 
#                  }

#         res = self.client.post(CHECKOUT_URL, data=params, format='json')
#         self.assertEqual(res.status_code, 201)