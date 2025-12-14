import re
import graphene
from django.db import IntegrityError
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Product, Order
from .filters import CustomerFilter, ProductFilter, OrderFilter


# ================= TYPES =================

class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        filterset_class = CustomerFilter
        interfaces = (graphene.relay.Node,)


class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        filterset_class = ProductFilter
        interfaces = (graphene.relay.Node,)


class OrderType(DjangoObjectType):
    class Meta:
        model = Order
        filterset_class = OrderFilter
        interfaces = (graphene.relay.Node,)


# ================= QUERIES =================

class Query(graphene.ObjectType):
    hello = graphene.String(default_value="Hello, GraphQL!")

    all_customers = DjangoFilterConnectionField(CustomerType)
    all_products = DjangoFilterConnectionField(ProductType)
    all_orders = DjangoFilterConnectionField(OrderType)


# ================= MUTATIONS =================

class CreateCustomer(graphene.Mutation):
    customer = graphene.Field(CustomerType)
    message = graphene.String()

    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    def mutate(self, info, name, email, phone=None):
        if phone and not re.match(r'^(\+\d{10,15}|\d{3}-\d{3}-\d{4})$', phone):
            raise Exception("Invalid phone format")

        try:
            customer = Customer.objects.create(
                name=name,
                email=email,
                phone=phone
            )
        except IntegrityError:
            raise Exception("Email already exists")

        return CreateCustomer(customer=customer, message="Customer created")


class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class BulkCreateCustomers(graphene.Mutation):
    customers = graphene.List(CustomerType)
    errors = graphene.List(graphene.String)

    class Arguments:
        input = graphene.List(CustomerInput, required=True)

    def mutate(self, info, input):
        created = []
        errors = []

        for idx, data in enumerate(input):
            try:
                customer = Customer.objects.create(**data)
                created.append(customer)
            except Exception as e:
                errors.append(f"Row {idx + 1}: {str(e)}")

        return BulkCreateCustomers(customers=created, errors=errors)


class CreateProduct(graphene.Mutation):
    product = graphene.Field(ProductType)

    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int()

    def mutate(self, info, name, price, stock=0):
        if price <= 0:
            raise Exception("Price must be positive")
        if stock < 0:
            raise Exception("Stock cannot be negative")

        product = Product.objects.create(
            name=name,
            price=price,
            stock=stock
        )
        return CreateProduct(product=product)


class CreateOrder(graphene.Mutation):
    order = graphene.Field(OrderType)

    class Arguments:
        customer_id = graphene.ID(required=True)
        product_ids = graphene.List(graphene.ID, required=True)

    def mutate(self, info, customer_id, product_ids):
        if not product_ids:
            raise Exception("At least one product required")

        customer = Customer.objects.get(pk=customer_id)
        products = Product.objects.filter(id__in=product_ids)

        if products.count() != len(product_ids):
            raise Exception("Invalid product ID")

        total = sum(p.price for p in products)

        order = Order.objects.create(
            customer=customer,
            total_amount=total
        )
        order.products.set(products)

        return CreateOrder(order=order)


class Mutation(graphene.ObjectType):
    create_customer = CreateCustomer.Field()
    bulk_create_customers = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    create_order = CreateOrder.Field()

