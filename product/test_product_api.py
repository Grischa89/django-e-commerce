from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from rating.models import Rating
from product.models import Product, Category

from rating.serializers import RatingSerializer


LATEST_PRODUCTS_URL =reverse('latest-products')
GENERAL_SEARCH_URL =reverse('search')
PRODUCT_DETAIL_URL =reverse('prodcut-detail', kwargs={'category_slug': 'summer', 'product_slug': 'slug_of_summer_product_1'})


def create_minimal_data():
    category_summer = Category.objects.create(name="summer", slug="summer")
    category_winter = Category.objects.create(name="winter", slug="winter")
    product1 = Product.objects.create(category=category_summer, name='summer_product_1'
                            ,slug='slug_of_summer_product_1',description='description for summer_product_1'
                            ,price=120.99)
    product2 = Product.objects.create(category=category_summer, name='summer_product_2'
                        ,slug='slug_of_summer_product_2',description='description for summer_product_2'
                        ,price=170.88)
    product3 = Product.objects.create(category=category_winter, name='winter_product_3'
                            ,slug='slug_of_winter_product_3',description='description for winter_product_3'
                            ,price=80.77)
    product4 = Product.objects.create(category=category_winter, name='winter_product_4'
                        ,slug='slug_of_winter_product_4',description='description for winter_product_4'
                        ,price=200.66)
    return product1, product2, product3, product4

class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.product1, self.product2, self.product3, self.product4 = create_minimal_data()

    def test_latest_product(self):
        """Test that login is not required to access the latest Products"""
        
        res = self.client.get(LATEST_PRODUCTS_URL) 
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 4)

    def test_search(self):
        """Test that login is not required to access the latest Products"""

        data ={'query':self.product1.name}
        res = self.client.post(GENERAL_SEARCH_URL, data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)

        data ={'query':'description'}
        res = self.client.post(GENERAL_SEARCH_URL, data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 4)

    def test_product_detail(self):
        """test that login is not required to access product detail"""

        PRODUCT_DETAIL_URL =reverse('prodcut-detail', kwargs={'category_slug': self.product1.category, 'product_slug': self.product1.slug })
        res = self.client.get(PRODUCT_DETAIL_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['id'], 1)
        self.assertEqual(res.data['name'], self.product1.name)
        self.assertEqual(res.data['description'], self.product1.description)
        self.assertEqual(float(res.data['price']), self.product1.price)

    def test_category(self):
        """test that login is not required to access category"""

        CATEGORY_URL =reverse('category', kwargs={'category_slug': 'summer'})
        res = self.client.get(CATEGORY_URL)
        self.assertEqual(res.status_code, 200)


class PrivateApiTests(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user=self.client.post('/api/v1/users/',data={'username':'mario','password':'i-keep-jumping'})
        print("self.user", self.user)
        # obtain a json web token for the newly created user
        response=self.client.post('/api/v1/token/login/',data={'username':'mario','password':'i-keep-jumping'})
        print("response111: ", response, response.data)
        self.token=response.data['auth_token']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_latest_product(self):
        """Test that logged in user can the the latest products"""
        product1, product2, product3, product4 = create_minimal_data()

        res = self.client.get(LATEST_PRODUCTS_URL) # check why get works
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 4)

    # def test_rate_product(self):
    #     """test if a registered user can rate a product"""
    #     category = Category.objects.create(name="summer", slug="summer")
    #     product = Product.objects.create(category=category, name='myproduct',slug='slug_of_my_product',
    #              description='description for tests',price=100.00)

    #     data = {'product':product.id, 'text':'example for a rating of a product', 'rate':5}
    #     res = self.client.post(RATE_PRODCUT_URL, data, format='json')

    #     print("test_create_product: ",  res.data)
    #     self.assertEqual(res.status_code, 201)
    #     self.assertEqual(res.data['id'], 1)
    #     self.assertEqual(res.data['product'], data['product'])
    #     self.assertEqual(res.data['text'], data['text'])
    #     self.assertEqual(res.data['rate'], data['rate'])