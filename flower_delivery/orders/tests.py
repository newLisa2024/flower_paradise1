from django.test import TestCase
from flower_delivery.orders.models import CustomUser, Product, Order

class ModelTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="testuser", email="test@example.com", password="testpassword", phone="1234567890")
        self.product = Product.objects.create(name="Rose", price=50, description="Fresh roses")
        self.order = Order.objects.create(user=self.user, status="Pending")

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.phone, "1234567890")

    def test_product_creation(self):
        self.assertEqual(self.product.name, "Rose")
        self.assertEqual(self.product.price, 50)

    def test_order_creation(self):
        self.assertEqual(self.order.user, self.user)
        self.assertEqual(self.order.status, "Pending")

