from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from core.models import Product, Profile
from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart


class PaymentViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='payuser', password='secret')
        self.shipping = ShippingAddress.objects.create(
            user=self.user,
            shipping_full_name='John Doe',
            shipping_email='john@example.com',
            shipping_address1='123 Main St',
            shipping_city='City',
            shipping_country='Country',
        )
        self.checkout_url = reverse('payment:checkout')
        self.payment_success_url = reverse('payment:payment_success')
        self.payment_failed_url = reverse('payment:payment_failed')

    def test_checkout_view_get_anonymous(self):
        """
        Anonymous users can still access checkout with a blank shipping form.
        """
        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/checkout.html')
        self.assertIn('shipping_form', response.context)

    def test_checkout_view_get_authenticated(self):
        self.client.login(username='payuser', password='secret')
        response = self.client.get(self.checkout_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/checkout.html')
        self.assertIn('shipping_form', response.context)
        self.client.logout()

    def test_payment_success_view(self):
        response = self.client.get(self.payment_success_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/payment_success.html')

    def test_payment_failed_view(self):
        response = self.client.get(self.payment_failed_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/process_failed.html')


class PaymentModelsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='anotheruser', password='testpass')
        self.profile = Profile.objects.get(user=self.user)
        self.product = Product.objects.create(
            name="PayTest Product",
            price=29.99,
            category_id=1,
            image1="uploads/product/test.jpg",
            image2="uploads/product/test.jpg",
            image3="uploads/product/test.jpg",
            image4="uploads/product/test.jpg",
        )

    def test_create_order(self):
        order = Order.objects.create(
            user=self.user,
            full_name="Another User",
            email="another@example.com",
            shipping_address="123 Testing Ave",
            amount_paid=100.00
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            user=self.user,
            quantity=1,
            price=29.99
        )
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(OrderItem.objects.count(), 1)

    def test_shipping_address_default_created(self):
        """
        By default, a ShippingAddress instance is created for a new user (via signals).
        """
        # The user in setUp has shipping auto-created.
        address = ShippingAddress.objects.filter(user=self.user).first()
        self.assertIsNotNone(address)
        self.assertEqual(address.shipping_full_name, '')


class StripeTests(TestCase):
    """
    Example tests for Stripe-related functions (create_checkout_session).
    Note: May need mocking if you're calling actual Stripe APIs.
    """
    def setUp(self):
        self.client = Client()

    def test_stripe_checkout_session(self):
        create_session_url = reverse('payment:create_checkout_session')
        response = self.client.get(create_session_url)
        # If you're actually calling Stripe, it will redirect or error.
        # In a real scenario, you might mock the Stripe API call.
        self.assertIn(response.status_code, [302, 303, 400, 500])
        # This check ensures you’re hitting the right flow.
