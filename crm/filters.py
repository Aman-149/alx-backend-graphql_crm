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
