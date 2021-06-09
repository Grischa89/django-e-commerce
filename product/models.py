from PIL import Image
from io import BytesIO

from django.core.files import File
from django.db import models

from django.contrib.auth.models import User # added by greg
from django.db.models import Avg

from autoslug import AutoSlugField
from rating.models import Rating

class Category(models.Model):
    name = models.CharField(max_length=255)
    # slug = models.SlugField()
    slug = AutoSlugField("Category Slug", unique=True, always_update=False, populate_from="name")

    class Meta:
        ordering = ('name', )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = AutoSlugField("Product Slug", unique=True, always_update=False, populate_from="name")
    description =models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail =models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    average_rating = models.FloatField( default=0) #blank=True
    counter_rating = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('-date_added', )

    def __str__(self):
        return self.name

    # @property
    # def price_exp(self):
    #     print("price_exp")
    #     return float(self.price) + float(1.50)

    # @property
    # def average_rating1(self):
    #     # Rating.objects.filter( product=request.data['product'] ).aggregate(Avg('rate'))
    #     print("avg works")
    #     print(self.id)
    #     print(Rating.objects.filter( product=self.id ).aggregate(Avg('rate')))
    #     print("cat: ", Category.objects.get(id=1))
    #     # print(self.productrating.aggregate(average_rating=Avg('rating'))['average_rating'])
    #     return self.rating.aggregate(average_rating=Avg('rating'))['average_rating']


    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        else:
            return ''
    
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url

            else:
                return ''

    
    def make_thumbnail(self, image, size=(300,200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail =File(thumb_io, name=image.name)

        return thumbnail