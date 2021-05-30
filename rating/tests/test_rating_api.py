from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from rating.models import Rating
from product.models import Product, Category

from rating.serializers import RatingSerializer


# INGREDIENTS_URL = 'products/rate_product/<slug:category_slug>/<slug:product_slug>/'
RATE_PRODCUT_URL =reverse('rate-product', kwargs={'category_slug': 'summer', 'product_slug': 'light-jacket'})


class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.post(RATE_PRODCUT_URL) # check why get works
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED) #todo


class PrivateApiTests(TestCase):
    """Test the private ingredients API"""

    def setUp(self):
        self.client = APIClient()
        self.user=self.client.post('/api/v1/users/',data={'username':'jana','password':'i-keep-jumping'})
        print("self.user", self.user)
        # obtain a json web token for the newly created user
        response=self.client.post('/api/v1/token/login/',data={'username':'jana','password':'i-keep-jumping'})
        print("response111: ", response, response.data)
        self.token=response.data['auth_token']
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_rate_product(self):
        """test if a registered user can rate a product"""
        category = Category.objects.create(name="summer", slug="summer")
        product = Product.objects.create(category=category, name='myproduct',slug='slug_of_my_product',
                 description='description for tests',price=100.00)

        data = {'product':product.id, 'text':'example for a rating of a product', 'rate':5}
        res = self.client.post(RATE_PRODCUT_URL, data, format='json')

        print("test_create_product: ",  res.data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.data['id'], 1)
        self.assertEqual(res.data['product'], data['product'])
        self.assertEqual(res.data['text'], data['text'])
        self.assertEqual(res.data['rate'], data['rate'])

        data = {'product':product.id, 'text':'example for a rating of a product', 'rate':'five is a string'}
        res1 = self.client.post(RATE_PRODCUT_URL, data, format='json')
        self.assertEqual(res1.status_code, 400)
        print(res1, "we print it", res1.data)

    def test_get_all_ratings_of_product(self):
        User = get_user_model()
        user = User.objects.get(username='jana')
        category = Category.objects.create(name="summer", slug="summer")
        product1 = Product.objects.create(category=category, name='myproduct',slug='slug_of_my_product',
                 description='description for tests',price=100.00)
        for i in range(2,5):
            Rating.objects.create(user=user, product=product1,
                    text="random rating text ", rate=i)
        RATINGS_URL =reverse('all-ratings', kwargs={'category_slug': category.slug, 'product_slug': product1.slug})
        res = self.client.get(RATINGS_URL)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 3)

        RATINGS_URL =reverse('all-ratings', kwargs={'category_slug': category.slug, 'product_slug': 'nonexistingproduct'})
        res1 = self.client.get(RATINGS_URL)
        self.assertEqual(res1.status_code, 404)



    def test___str__(self):
        
        User = get_user_model()
        user = User.objects.get(username='jana')
        category_summer = Category.objects.create(name="summer", slug="summer")
        product1 = Product.objects.create(category=category_summer, name='summer_product_1'
                            ,slug='slug_of_summer_product_1',description='description for summer_product_1'
                            ,price=120.99)
        rating1 = Rating.objects.create(user=user, product=product1,
                        text="first rating", rate=5)
        self.assertEqual(rating1.__str__() , 'user={0}, product={1}, text={2}, rate={3}'.format(rating1.user, rating1.product, rating1.text, rating1.rate))