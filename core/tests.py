from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Product, Category
from django.contrib import messages


class CoreViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Test Category")
        self.product = Product.objects.create(
            name="Test Product",
            price=10.99,
            category=self.category,
            image1="uploads/product/sample.jpg",
            image2="uploads/product/sample.jpg",
            image3="uploads/product/sample.jpg",
            image4="uploads/product/sample.jpg",
        )
        self.index_url = reverse('core:index')
        self.category_url = reverse('core:category', args=[self.category.name.replace(' ', '-')])
        self.product_url = reverse('core:product-detail', args=[self.product.id])
        self.contact_url = reverse('core:contact')

    def test_index_view(self):
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertIn('products', response.context)

    def test_category_view(self):
        response = self.client.get(self.category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        self.assertIn('products', response.context)

    def test_product_detail_view(self):
        response = self.client.get(self.product_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product-detail.html')
        self.assertIn('product', response.context)
        self.assertEqual(response.context['product'].name, "Test Product")

    def test_contact_form_post(self):
        """
        Check contact form logic — currently sending an email or rendering a success message.
        """
        post_data = {
            'message-name': 'John Doe',
            'message-email': 'johndoe@example.com',
            'message-subject': 'Hello',
            'message': 'Test message content'
        }
        response = self.client.post(self.contact_url, post_data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')
        self.assertIn('Thanks John Doe!', response.content.decode())

   
class CoreModelsTests(TestCase):
    def test_category_str(self):
        cat = Category.objects.create(name="Sample")
        self.assertEqual(str(cat), "Sample")

    def test_product_str(self):
        cat = Category.objects.create(name="Sample")
        prod = Product.objects.create(
            name="Item123",
            price=9.99,
            category=cat,
            image1="uploads/product/item.jpg",
            image2="uploads/product/item.jpg",
            image3="uploads/product/item.jpg",
            image4="uploads/product/item.jpg",
        )
        self.assertEqual(str(prod), "Item123")
