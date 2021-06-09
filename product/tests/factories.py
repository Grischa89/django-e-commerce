# from PIL import Image
# from io import BytesIO

import factory
import factory.fuzzy

from django.core.files import File
from django.core.files.base import ContentFile

from ..models import Product, Category

class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.fuzzy.FuzzyChoice(
    [x[0] for x in ['summer', 'winter']]
    )
    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory):
    # category = factory.fuzzy.FuzzyChoice(
    # [x[0] for x in ['summer', 'winter']]
    # )
    category =  factory.SubFactory(CategoryFactory)
    name = factory.fuzzy.FuzzyText()
    description = factory.Faker('paragraph', nb_sentences=3,) 
    price = factory.fuzzy.FuzzyDecimal(4.99, 499.99)
    image = factory.LazyAttribute(
            lambda _: ContentFile(
                factory.django.ImageField()._make_data(
                    {'width': 1024, 'height': 768}
                ), 'exampleJana.jpg'
            )
        )
        
    class Meta:
        model = Product

