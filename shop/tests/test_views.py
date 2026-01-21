# shop/tests/test_views.py

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from shop.models import Product, Order, OrderItem


class CartViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="Laptop", price=999.99)

    def test_cart_add(self):
        response = self.client.post(reverse('cart_add', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)  # redirects
        cart = self.client.session['cart']
        self.assertIn(str(self.product.id), cart)

    def test_cart_remove(self):
        self.client.post(reverse('cart_add', args=[self.product.id]))
        response = self.client.get(reverse('cart_remove', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)
        cart = self.client.session['cart']
        self.assertNotIn(str(self.product.id), cart)

    def test_cart_update(self):
        self.client.post(reverse('cart_add', args=[self.product.id]))
        response = self.client.post(reverse('cart_update', args=[self.product.id]), {'quantity': 3})
        self.assertEqual(response.status_code, 302)
        cart = self.client.session['cart']
        self.assertEqual(cart[str(self.product.id)]['quantity'], 3)

    def test_cart_detail_view(self):
        self.client.post(reverse('cart_add', args=[self.product.id]))
        response = self.client.get(reverse('cart_detail'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Laptop")
class CheckoutViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='john', password='pass123')
        self.product = Product.objects.create(name="Phone", price=500)

    def test_checkout_redirects_if_not_logged_in(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # should redirect to login

    def test_checkout_with_empty_cart(self):
        self.client.login(username='john', password='pass123')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # redirects back to product list

    def test_checkout_success(self):
        self.client.login(username='john', password='pass123')
        session = self.client.session
        session['cart'] = {
            str(self.product.id): {'name': self.product.name, 'price': float(self.product.price), 'quantity': 2}
        }
        session.save()
        response = self.client.post(reverse('checkout'))
        self.assertEqual(response.status_code, 302)  # redirect after order
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)
class RegisterViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_page_loads(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_user_success(self):
        response = self.client.post(reverse('register'), {
            'username': 'alice',
            'email': 'alice@example.com',   # add if required by form
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
        })
        # After successful register, should redirect
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username='alice').exists())
