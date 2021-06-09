from django.test import TestCase
from django.urls import reverse
from .factories import ProductFactory, CategoryFactory
from ..models import Product, Category
from rest_framework.test import APIClient


from django.conf import settings 


class ProductModelTest(TestCase):
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
        self.category_summer = CategoryFactory(name="summer")
        self.product = ProductFactory(category=self.category_summer,
                                      name="Sample product")
        self.create_product_with_thumbnail()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_product___str__(self):
        """test product and category return value"""
        self.assertEqual(self.product.__str__(), self.product.name)
        self.assertEqual(self.category_summer.__str__(), self.category_summer.name)
        self.assertEqual('/{0}/{1}/'.format(self.category_summer.name, self.product.slug), self.product.get_absolute_url())
        self.assertEqual('/{0}/'.format(self.category_summer.slug), self.category_summer.get_absolute_url())

    
    def test_image_url(self):  
        """ test existing image url"""
        print("settings.MEDIA_ROOT", settings.MEDIA_ROOT)
        print("MEDIA_URL: ", settings.MEDIA_URL)
        image_url = 'http://127.0.0.1:8000/media/{0}'.format(self.product.image.name)
        self.assertEqual(self.product.get_image(), image_url)

    def test_thumbnail_url(self):  
        """ test existing thumbnail url"""
        thumbnail_url = 'http://127.0.0.1:8000/media/uploads/{0}'.format(self.product.image.name)
        self.assertEqual(self.product.get_thumbnail(), thumbnail_url)

        url_1 = 'uploads/{0}'.format(self.product.image.name)
        # self.assertEqual(str(self.product.thumbnail), url_1)
    def test_product_without_image_and_thumbnail(self):  
        """ test non existing image url and thumbnail"""
        product_without_picture = ProductFactory(category=self.category_summer, name="Sample product no picture",
                                                   image="" )
        self.assertEqual(product_without_picture.get_image(), '')
        self.assertEqual(product_without_picture.get_thumbnail(), '')

    def test_get_thumnail_after_request(self):
        """test thumbnail gets created from product with picture after get request"""
        thumbnail_url = 'http://127.0.0.1:8000/media/uploads/{0}'.format(self.product.image.name)
        PRODUCT_DETAIL_URL =reverse('prodcut-detail', kwargs={'category_slug': self.category_summer.slug, 'product_slug': self.product.slug})
        
        res = self.client.get(PRODUCT_DETAIL_URL)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['get_thumbnail'], thumbnail_url)

    def create_product_with_thumbnail(self):
        """create product with thumbnail because get request leads to creation of thumbnail"""
        self.product_with_thumbnail = ProductFactory(category=self.category_summer, name="product_with_thumbnail")
        PRODUCT_DETAIL_URL =reverse('prodcut-detail', kwargs={'category_slug': self.category_summer.slug, 'product_slug': self.product_with_thumbnail.slug})
        res = self.client.get(PRODUCT_DETAIL_URL)

    def test_existing_thumbnail(self):
        
        PRODUCT_DETAIL_URL=reverse('prodcut-detail',
                           kwargs={
                            'category_slug':self.category_summer.slug,
                            'product_slug':self.product_with_thumbnail.slug
                            }
                            )
        res = self.client.get(PRODUCT_DETAIL_URL)

        thumbnail_url = 'http://127.0.0.1:8000/media/uploads/{0}'.format(self.product_with_thumbnail.image.name)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data['get_thumbnail'], thumbnail_url)









