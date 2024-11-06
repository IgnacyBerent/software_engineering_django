from django.db import models
from django.core.validators import MinValueValidator

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0.01)])
    available = models.BooleanField(default=True)

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)

class Order(models.Model):
    STATUS_CHOICES = [
        ('New', 'New'),
        ('In Process', 'In Process'),
        ('Sent', 'Sent'),
        ('Completed', 'Completed'),
    ]

    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    date = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)

    def total_price(self):
        return sum([product.price for product in self.products.all()])
    
    def can_be_fullfilled(self):
        return all([product.available for product in self.products.all()])