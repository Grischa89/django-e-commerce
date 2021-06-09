import factory
from factory.declarations import SelfAttribute
import factory.fuzzy
from faker import Factory

from django.core.files import File
from django.core.files.base import ContentFile

from ..models import Order, OrderItem
from factory.django import DjangoModelFactory
from django.contrib.auth.models import  User
from product.tests.factories import ProductFactory
import datetime

faker = Factory.create()

class UserFactory(DjangoModelFactory):
    username = "Factory User Sample"
    password = factory.PostGenerationMethodCall(
        'set_password',
        faker.password(
            length=10,
            special_chars=True,
            digits=True,
            upper_case=True,
            lower_case=True,
        )
    )

    class Meta:
        model = User

class OrderFactory(factory.django.DjangoModelFactory):

    user = factory.SubFactory(UserFactory)
    first_name = factory.Sequence(lambda n: 'J%shn' % ('o' * (n+1)))
    last_name = factory.Sequence(lambda n: 'D%se' % ('o' * (n+1)))
    email = factory.LazyAttribute(
            lambda o: '%s.%s@example.de' % (o.first_name, o.last_name)
            )
    address = factory.LazyAttribute(
            lambda o: '%s Street %s' % (o.first_name, len(o.last_name))
            )
    zipcode = factory.fuzzy.FuzzyInteger(10000, 99999)
    place = factory.LazyAttribute(
            lambda o: '%sland' % (o.last_name)
            )
    phone = factory.fuzzy.FuzzyInteger(10000, 99998)
    created_at = factory.fuzzy.FuzzyDate(datetime.date(2018, 1, 1))
    stripe_token = factory.fuzzy.FuzzyText(length=28, prefix="Stripe_token:")
    
    class Meta:
        model = Order

    @factory.post_generation
    def orderitems(self, create, extracted, **kwargs):
        if not create:
            return
        self.paid_amount = 0
        if extracted:
            for item in extracted:
                orderitem = OrderItemFactory.create(order=self, product=item)            
                self.paid_amount += orderitem.price


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem
    
    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    price = factory.SelfAttribute('product.price')
    quantity = factory.fuzzy.FuzzyInteger(1, 3)
    


