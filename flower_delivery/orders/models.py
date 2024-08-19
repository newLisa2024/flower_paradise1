from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Укажите уникальное имя для related_name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  # Укажите уникальное имя для related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )


def product_image_upload_path(instance, filename):
    # Путь для сохранения загружаемых изображений в папку static/products
    return f'products/{filename}'

class Product(models.Model):
    name = models.CharField('Название букета', max_length=50)
    price = models.DecimalField('Стоимость', max_digits=10, decimal_places=2)
    image = models.ImageField('Фото', upload_to=product_image_upload_path, blank=True, null=True)
    description = models.TextField('Описание')
    class Meta:
        verbose_name = 'Букет'
        verbose_name_plural = 'Букеты'

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        return self.quantity * self.product.price

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'В ожидании'),
        ('Processing', 'В обработке'),
        ('Shipped', 'Отправлен'),
        ('Delivered', 'Доставлен'),
        ('Cancelled', 'Отменен'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Убедитесь, что указано правильно
    products = models.ManyToManyField(Product)  # Это поле ManyToMany, проблем здесь быть не должно
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=100, blank=True, null=True)
    delivery_address = models.TextField(blank=True, null=True)

    def total_price(self):
        return sum(item.get_total_price() for item in self.orderitem_set.all())

    total_price.short_description = 'Total Price'
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total_price(self):
        return self.quantity * self.price

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"



