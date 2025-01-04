from django.test import TestCase
from myapp.models import Product, Customer, Order
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError, DataError


class ProductModelTest(TestCase):
    def test_create_product_with_valid_data(self):
        temp_product = Product.objects.create(
            name="Temporary product", price=1.99, available=True
        )
        self.assertEqual(temp_product.name, "Temporary product")
        self.assertEqual(temp_product.price, 1.99)
        self.assertTrue(temp_product.available)

    def test_create_product_with_negative_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name="Invalid product", price=-1.99, available=True
            )
            temp_product.full_clean()

    def test_create_product_with_empty_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name="", price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_missing_price(self):
        with self.assertRaises(IntegrityError):
            temp_product = Product.objects.create(
                name="Invalid product", available=True
            )
            temp_product.full_clean()

    def test_create_product_with_missing_availability(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(name="Invalid product", price=1.99)
            temp_product.full_clean()

    def test_create_product_with_missing_name(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(price=1.99, available=True)
            temp_product.full_clean()

    def test_create_product_with_boundary_name(self):
        temp_product = Product.objects.create(
            name="a" * 255, price=1.99, available=True
        )
        self.assertEqual(temp_product.name, "a" * 255)

    def test_create_product_with_too_long_name(self):
        with self.assertRaises(DataError):
            temp_product = Product.objects.create(
                name="a" * 256, price=1.99, available=True
            )
            temp_product.full_clean()

    def test_create_product_with_boundary_price(self):
        temp_product = Product.objects.create(
            name="Boundary price product", price=0.01, available=True
        )
        self.assertEqual(temp_product.price, 0.01)

    def test_create_product_with_too_small_price(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name="Invalid product", price=0.0, available=True
            )
            temp_product.full_clean()

    def test_create_product_with_too_high_price(self):
        with self.assertRaises(DataError):
            temp_product = Product.objects.create(
                name="Invalid product", price=100000.00, available=True
            )
            temp_product.full_clean()

    def test_create_product_with_invalid_price_format(self):
        with self.assertRaises(ValidationError):
            temp_product = Product.objects.create(
                name="Invalid product", price=1.999, available=True
            )
            temp_product.full_clean()


class CustomerModelTest(TestCase):
    def test_create_customer_with_valid_data(self):
        temp_customer = Customer.objects.create(
            name="Temporary customer", address="Swidnicka 2, 50-345 Wroclaw"
        )
        self.assertEqual(temp_customer.name, "Temporary customer")
        self.assertEqual(temp_customer.address, "Swidnicka 2, 50-345 Wroclaw")

    def test_create_customer_with_empty_name(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(
                name="", address="Swidnicka 2, 50-345 Wroclaw"
            )
            temp_customer.full_clean()

    def test_create_customer_with_missing_address(self):
        with self.assertRaises(ValidationError):
            temp_customer = Customer.objects.create(name="Invalid customer")
            temp_customer.full_clean()

    def test_create_customer_with_edge_name(self):
        temp_customer = Customer.objects.create(
            name="a" * 100, address="Swidnicka 2, 50-345 Wroclaw"
        )
        self.assertEqual(temp_customer.name, "a" * 100)

    def test_create_customer_with_too_long_name(self):
        with self.assertRaises(DataError):
            temp_customer = Customer.objects.create(
                name="a" * 101, address="Swidnicka 2, 50-345 Wroclaw"
            )
            temp_customer.full_clean()


class OrderModelTest(TestCase):
    def setUp(self):
        self.temp_customer = Customer.objects.create(
            name="Temporary customer", address="Swidnicka 2, 50-345 Wroclaw"
        )

        self.temp_product1 = Product.objects.create(
            name="Temporary product 1", price=1.99, available=True
        )

        self.temp_product2 = Product.objects.create(
            name="Temporary product 2", price=2.99, available=True
        )

        self.temp_product3 = Product.objects.create(
            name="Temporary product 3", price=3.99, available=False
        )

    def test_create_order_with_valid_data(self):
        temp_order = Order.objects.create(
            customer=self.temp_customer,
            date="2025-01-01",
            status="New",
        )
        temp_order.products.set([self.temp_product1, self.temp_product2])

        self.assertEqual(temp_order.customer, self.temp_customer)
        self.assertQuerySetEqual(
            temp_order.products.all(),
            [self.temp_product1, self.temp_product2],
            ordered=False,
        )
        self.assertEqual(temp_order.date, "2025-01-01")
        self.assertEqual(temp_order.status, "New")

    def test_create_order_with_missing_customer(self):
        with self.assertRaises(IntegrityError):
            temp_order = Order.objects.create(date="2025-01-01", status="New")
            temp_order.products.set([self.temp_product1, self.temp_product2])
            temp_order.full_clean()

    def test_create_order_with_invalid_status(self):
        with self.assertRaises(ValidationError):
            temp_order = Order.objects.create(
                customer=self.temp_customer, date="2025-01-01", status="Invalid"
            )
            temp_order.products.set([self.temp_product1, self.temp_product2])
            temp_order.full_clean()

    def test_order_total_price_with_valid_products(self):
        temp_order = Order.objects.create(
            customer=self.temp_customer,
            date="2025-01-01",
            status="New",
        )
        temp_order.products.set([self.temp_product1, self.temp_product2])

        self.assertEqual(
            float(temp_order.total_price()),
            self.temp_product1.price + self.temp_product2.price,
        )

    def test_order_total_price_with_no_products(self):
        temp_order = Order.objects.create(
            customer=self.temp_customer,
            date="2025-01-01",
            status="New",
        )

        self.assertEqual(float(temp_order.total_price()), 0.0)

    def test_order_can_be_fullfilled(self):
        temp_order = Order.objects.create(
            customer=self.temp_customer,
            date="2025-01-01",
            status="New",
        )
        temp_order.products.set([self.temp_product1, self.temp_product2])

        self.assertTrue(temp_order.can_be_fullfilled())

    def test_order_cannot_be_fullfilled(self):
        temp_order = Order.objects.create(
            customer=self.temp_customer,
            date="2025-01-01",
            status="New",
        )
        temp_order.products.set(
            [self.temp_product1, self.temp_product2, self.temp_product3]
        )

        self.assertFalse(temp_order.can_be_fullfilled())
