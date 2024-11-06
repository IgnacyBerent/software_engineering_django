from django.core.management.base import BaseCommand
from myapp.models import Product, Customer, Order
from datetime import date

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        # Delete existing entries
        Product.objects.all().delete()
        Customer.objects.all().delete()
        Order.objects.all().delete()

        # Create Product entries
        product1 = Product.objects.create(name='Product 1', price=19.99, available=True)
        product2 = Product.objects.create(name='Product 2', price=29.99, available=True)
        product3 = Product.objects.create(name='Product 3', price=39.99, available=False)

        # Create Customer entries
        customer1 = Customer.objects.create(name='Customer 1', address='123 Main St')
        customer2 = Customer.objects.create(name='Customer 2', address='456 Elm St')
        customer3 = Customer.objects.create(name='Customer 3', address='789 Oak St')

        # Create Order entries
        order1 = Order.objects.create(customer=customer1, date=date.today(), status='New')
        order2 = Order.objects.create(customer=customer2, date=date.today(), status='In Process')
        order3 = Order.objects.create(customer=customer3, date=date.today(), status='Completed')

        # Add products to orders
        order1.products.add(product1, product2)
        order2.products.add(product2, product3)
        order3.products.add(product1, product3)

        self.stdout.write("Data created successfully.")