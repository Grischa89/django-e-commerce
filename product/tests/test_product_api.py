from django.test import TestCase
from django.urls import reverse
from .factories import ProductFactory, CategoryFactory
from rest_framework.test import APIClient

LATEST_PRODUCTS_URL =reverse('latest-products')
GENERAL_SEARCH_URL =reverse('search')

class PublicIngredientsApiTests(TestCase):
    """Test the publicly available ingredients API"""

    def setUp(self):
        self.client = APIClient()
        
        self.category_summer = CategoryFactory(name="summer")
        self.category_winter = CategoryFactory(name="winter")
        self.product1 = ProductFactory(category=self.category_summer,
                                       name="Sample product 1",
                                       description="Sample product 1 descirption"
                                       )
        self.create_product(number=3)

    def create_product(self, number):
        for count in range(0, number):
            if (count % 2) == 0:
                ProductFactory(category=self.category_summer,
                               name=f"Sample product {count}")
            else:
                ProductFactory(category=self.category_winter,
                               name=f"Sample product {count}")


    def test_latest_product(self):
        """Test that login is not required to access the latest Products"""
        
        res = self.client.get(LATEST_PRODUCTS_URL) 
        self.assertEqual(res.status_code, 200)
        self.assertLessEqual(len(res.data), 4)

    def test_search_by_name(self):
        """Test that login is not required to access search (name)"""

        data ={'query':self.product1.name}
        res = self.client.post(GENERAL_SEARCH_URL, data)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

    def test_search_by_description(self):
        """Test that login is not required to access search (description)"""
        data ={'query':self.product1.description}
        res = self.client.post(GENERAL_SEARCH_URL, data)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

    def test_search_without_return(self):
        """Test that search can return zero products"""
        # data ={'query':"!%$üäöyxz089"}
        data ={'query':""}
        res = self.client.post(GENERAL_SEARCH_URL, data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['products']), 0)

    def test_product_detail(self):
        """test that login is not required to access product detail"""
        PRODUCT_DETAIL_URL = reverse('prodcut-detail', 
                             kwargs={'category_slug': self.product1.category,
                                     'product_slug': self.product1.slug })
        res = self.client.get(PRODUCT_DETAIL_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['id'], 1)
        self.assertEqual(res.data['name'], self.product1.name)
        self.assertEqual(res.data['description'], self.product1.description)
        self.assertEqual(res.data['price'], str(self.product1.price))

    def test_non_existing_product(self):
        """Test that Http404 is returned for not existing Product"""
        PRODUCT_DETAIL_URL = reverse('prodcut-detail', 
                             kwargs={'category_slug': self.product1.category,
                                     'product_slug': "non-existing-product" })
        res = self.client.get(PRODUCT_DETAIL_URL)
        self.assertEqual(res.status_code, 404)

    def test_category(self):
        """test that login is not required to access category"""

        CATEGORY_URL = reverse('category', 
                       kwargs={'category_slug': self.product1.category})

        res = self.client.get(CATEGORY_URL)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

    def test_non_existing_category(self):
        """test Http404 is returned for not existing Category"""

        CATEGORY_URL = reverse('category', 
                       kwargs={'category_slug': "not-existing-categoryyy"})

        res = self.client.get(CATEGORY_URL)
        self.assertEqual(res.status_code, 404)

################################

class PrivateProductApiTests(TestCase):
    """Test the private ingredients API"""

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
        self.category_summer = CategoryFactory(name="summer")
        self.category_winter = CategoryFactory(name="winter")
        self.product1 = ProductFactory(category=self.category_summer,
                                       name="Sample product 1",
                                       description="Sample product 1 descirption"
                                       )

        self.create_product(number=3)

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def create_product(self, number):
        for count in range(0, number):
            if (count % 2) == 0:
                ProductFactory(category=self.category_summer,
                               name=f"Sample product {count}")
            else:
                ProductFactory(category=self.category_winter,
                               name=f"Sample product {count}")

    def test_latest_product(self):
        """Test that logged in user can use latest products"""

        res = self.client.get(LATEST_PRODUCTS_URL) 
        self.assertEqual(res.status_code, 200)
        self.assertLessEqual(len(res.data), 4)


    def test_search_by_name(self):
        """Test that logged in user can search by (name)"""

        data ={'query':self.product1.name}
        res = self.client.post(GENERAL_SEARCH_URL, data)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

    def test_search_by_description(self):
        """Test that logged in user can search by (description)"""
        data ={'query':self.product1.description}
        res = self.client.post(GENERAL_SEARCH_URL, data)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)

    def test_product_detail(self):
        """Test that logged in user can access product detail"""

        PRODUCT_DETAIL_URL = reverse('prodcut-detail', 
                             kwargs={'category_slug': self.product1.category,
                                     'product_slug': self.product1.slug })
        res = self.client.get(PRODUCT_DETAIL_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['id'], 1)
        self.assertEqual(res.data['name'], self.product1.name)
        self.assertEqual(res.data['description'], self.product1.description)
        self.assertEqual(res.data['price'], str(self.product1.price))

    def test_category(self):
        """Test that logged in user can access category"""

        CATEGORY_URL = reverse('category', 
                       kwargs={'category_slug': self.product1.category})
        res = self.client.get(CATEGORY_URL)
        self.assertEqual(res.status_code, 200)
        self.assertGreaterEqual(len(res.data), 1)