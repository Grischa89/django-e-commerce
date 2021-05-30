# import pytest

from ..models import Product, Category
# pytestmark = pytest.mark.django_db


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

def test___str__():
    product1 = Product.objects.create(category=category_summer, name='summer_product_1'
                        ,slug='slug_of_summer_product_1',description='description for summer_product_1'
                        ,price=120.99)
    assertEqual(product1.__str__(), "summer_product_1")

def test___str__():
    product1 = Product.objects.create(category=category_summer, name='summer_product_1'
                        ,slug='slug_of_summer_product_1',description='description for summer_product_1'
                        ,price=120.99)
    assertEqual(product1.__str__(), "summer_product_1")