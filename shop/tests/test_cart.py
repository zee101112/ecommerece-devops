from django.test import TestCase
from django.urls import reverse
from shop.models import Product

class CartTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop",
            description="Gaming laptop",
            price=1200,
            stock=3
        )

    def test_add_to_cart(self):
        response = self.client.post(reverse("cart_add", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # redirect after adding
        cart = self.client.session.get("cart")
        self.assertIn(str(self.product.id), cart)
