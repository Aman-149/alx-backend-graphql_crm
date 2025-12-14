import django_filters
from .models import Customer, Product, Order

class CustomerFilter(django_filters.FilterSet):
    phone_pattern = django_filters.CharFilter(
        field_name='phone',
        lookup_expr='startswith'
    )

    class Meta:
        model = Customer
        fields = {
            'name': ['icontains'],
            'email': ['icontains'],
            'created_at': ['gte', 'lte'],
        }


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'name': ['icontains'],
            'price': ['gte', 'lte'],
            'stock': ['gte', 'lte'],
        }


class OrderFilter(django_filters.FilterSet):
    customer_name = django_filters.CharFilter(
        field_name='customer__name',
        lookup_expr='icontains'
    )
    product_name = django_filters.CharFilter(
        field_name='products__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Order
        fields = {
            'total_amount': ['gte', 'lte'],
            'order_date': ['gte', 'lte'],
        }

import django_filters
from .models import Customer

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['name', 'email']
import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer
from .filters import CustomerFilter


# ================= Customer Node =================

class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node,)
        filterset_class = CustomerFilter
        fields = ("id", "name", "email", "phone")


# ================= Query =================

class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerNode)


import graphene
from graphene import relay
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer
from .filters import CustomerFilter


# ---------------- Customer Node ----------------
class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (relay.Node,)
        filterset_class = CustomerFilter
        fields = ("id", "name", "email", "phone")


# ---------------- Query ----------------
class Query(graphene.ObjectType):
    all_customers = DjangoFilterConnectionField(CustomerNode)

import django_filters
from .models import Customer

class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = Customer
        fields = ['name', 'email']
