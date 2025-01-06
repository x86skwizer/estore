from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from core.models import Product, Category
from .cart import Cart
from .views import cart_summary


class CartTests(TestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='secret')
        self.client = Client()
        # Create category and product
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            price=10.99,
            category=self.category,
            description="Sample description",
            image1="uploads/product/sample.jpg",
            image2="uploads/product/sample.jpg",
            image3="uploads/product/sample.jpg",
            image4="uploads/product/sample.jpg",
        )
        self.cart_url = reverse('cart:cart_summary')
        self.add_url = reverse('cart:cart_add')

    def test_cart_context_processor(self):
        """
        Ensure the cart is in context for every page.
        """
        response = self.client.get(self.cart_url)
        self.assertIn('cart', response.context)

    def test_cart_add(self):
        """
        Test adding a product to the cart via AJAX POST.
        """
        post_data = {
            'product_id': self.product.id,
            'product_qty': 2,
            'action': 'post'
        }
        response = self.client.post(self.add_url, post_data, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        # Check JSON response
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Product added to cart successfully.')

    def test_cart_summary_view_unauthenticated(self):
        """
        Cart page should load for unauthenticated users too.
        """
        response = self.client.get(self.cart_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart_summary.html')

    def test_cart_integration(self):
        """
        Test direct usage of Cart class. 
        """
        session = self.client.session
        cart_obj = Cart(self.client.request().wsgi_request)
        cart_obj.add(self.product, 3)
        self.assertEqual(len(cart_obj), 3)  # quantity should be 3
        self.assertEqual(cart_obj.cart_total(), 3 * self.product.price)
