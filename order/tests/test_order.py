from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from stripe.six import assertCountEqual
from .factories import  OrderFactory
from order.views import checkout
from product.tests.factories import ProductFactory, CategoryFactory
from rest_framework.test import APIClient
from unittest import mock

CHECKOUT_URL = reverse('checkout')

class PublicOrderModelTest(TestCase):
    """Test the product model in not logged in """

    def setUp(self):
        self.client = APIClient()
        self.user = self.client.post('/api/v1/users/', data={
                                    'username':'jana',
                                    'password':'1-keep-c0ding'
                                    })

        User = get_user_model()
        user = User.objects.get(username='jana')
        self.category_summer = CategoryFactory(name="summer")
        self.product = ProductFactory(category=self.category_summer,
                                      name="Sample product")
        self.product1 = ProductFactory(category=self.category_summer,
                                      name="Sample product 1")
  
        self.order1 = OrderFactory(user=user)


    @mock.patch("order.views.stripe.Charge.create")
    def test_checkout_success(self, mock_event_create):
        """ test checkout success """
        #todo rheinfolge verändern und namen und beschreibung ändern
        mock_event_create.return_value = "WE THE BEST MUSIC"
        
        params = {'first_name': self.order1.first_name,
                 'last_name': self.order1.last_name, 
                 'email': self.order1.email,
                 'address': self.order1.address,
                 'zipcode': self.order1.zipcode,
                 'place': self.order1.place,
                 'phone': self.order1.phone,
                 'items': [{
                 'product': self.product1.id,
                 'quantity': 1,
                 'price': self.product1.price
                 },
                 {'product': self.product.id,
                 'quantity': 1,
                 'price':self.product.price}
                 ],
                 'stripe_token': self.order1.stripe_token # 'tok_1IzaoBHsFtjiaIoWWGDQGREG'
                 }

        res = self.client.post(CHECKOUT_URL, data=params, format='json')
        self.assertEqual(res.status_code, 401)

    @mock.patch("order.views.stripe.Charge.create")
    def test_checkout_error(self, mock_event_create):
        """ test checkout failure """
        mock_event_create.return_value = "WE THE BEST MUSIC"

        params = {'first_name': self.order1.first_name,
                 'last_name': self.order1.last_name, 
                 'email': self.order1.email,
                 'address': self.order1.address,
                 'zipcode': self.order1.zipcode,
                 'place': self.order1.place,
                 'phone': self.order1.phone,
                 'items': [{
                 'product': self.product1.id + 122,
                 'quantity': 1,
                 'price': self.product1.price
                 },
                 {'product': self.product.id + 123,
                 'quantity': 1,
                 'price':self.product.price}
                 ],
                 'stripe_token': self.order1.stripe_token # 'tok_1IzaoBHsFtjiaIoWWGDQGREG'
                 }

        res = self.client.post(CHECKOUT_URL, data=params, format='json')
        self.assertEqual(res.status_code, 401)
    
    def test_get_orders_list(self):
        """ test get OrdersList successfull"""

        ORDERS_LIST = reverse("orders")
        res = self.client.get(ORDERS_LIST)
        self.assertEqual(res.status_code, 401)

class PrivateOrderModelTest(TestCase):
    """Test the product model"""

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
  
        self.order1 = OrderFactory(user=user)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    @mock.patch("order.views.stripe.Charge.create")
    def test_order___str__(self, mock_event_create):
        """ test checkout success """
        mock_event_create.return_value = "WE THE BEST MUSIC"
        
        params = {'first_name': self.order1.first_name,
                 'last_name': self.order1.last_name, 
                 'email': self.order1.email,
                 'address': self.order1.address,
                 'zipcode': self.order1.zipcode,
                 'place': self.order1.place,
                 'phone': self.order1.phone,
                 'items': [{
                 'product': self.product1.id,
                 'quantity': 1,
                 'price': self.product1.price
                 },
                 {'product': self.product.id,
                 'quantity': 1,
                 'price':self.product.price}
                 ],
                 'stripe_token': self.order1.stripe_token 
                 }
        
        res = self.client.post(CHECKOUT_URL, data=params, format='json')
        self.assertEqual(res.status_code, 201)


    @mock.patch("order.views.stripe.Charge.create")
    def test_checkout_error(self, mock_event_create):
        """ test checkout failure """
        mock_event_create.return_value = "WE THE BEST MUSIC"

        params = {'first_name': self.order1.first_name,
                 'last_name': self.order1.last_name, 
                 'email': self.order1.email,
                 'address': self.order1.address,
                 'zipcode': self.order1.zipcode,
                 'place': self.order1.place,
                 'phone': self.order1.phone,
                 'items': [{
                 'product': self.product1.id + 122,
                 'quantity': 1,
                 'price': self.product1.price
                 },
                 {'product': self.product.id + 123,
                 'quantity': 1,
                 'price':self.product.price}
                 ],
                 'stripe_token': self.order1.stripe_token # 'tok_1IzaoBHsFtjiaIoWWGDQGREG'
                 }

        res = self.client.post(CHECKOUT_URL, data=params, format='json')
        self.assertEqual(res.status_code, 400)

    @mock.patch("order.views.stripe.Charge.create")
    def test_checkout_stripe_exception(self, mock_event_create):
        # from apiclient.errors import HttpError

        """ test checkout stripe_exception """
        mock_event_create.return_value = "WE THE BEST MUSIC"
        mock_event_create.side_effect = Exception() 

        params = {'first_name': self.order1.first_name,
                 'last_name': self.order1.last_name, 
                 'email': self.order1.email,
                 'address': self.order1.address,
                 'zipcode': self.order1.zipcode,
                 'place': self.order1.place,
                 'phone': self.order1.phone,
                 'items': [{
                 'product': self.product1.id,
                 'quantity': 1,
                 'price': self.product1.price
                 },
                 {'product': self.product.id,
                 'quantity': 1,
                 'price':self.product.price}
                 ],
                 'stripe_token': self.order1.stripe_token
                 }

        res = self.client.post(CHECKOUT_URL, data=params, format='json')
        self.assertEqual(res.status_code, 400)
    
    def test_get_orders_list(self):
        """ test get OrdersList successfull"""

        ORDERS_LIST = reverse("orders")
        res = self.client.get(ORDERS_LIST)
        self.assertEqual(res.status_code, 200)


