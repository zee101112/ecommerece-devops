from django.test import TestCase
from shop.models import Product

class ProductModelTest(TestCase):
    def test_product_str(self):
        product = Product.objects.create(
            name="Test Product",
            description="A test product",
            price=99.99,
            stock=10
        )
        self.assertEqual(str(product), "Test Product")
