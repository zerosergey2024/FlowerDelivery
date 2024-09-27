# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Модель Product представляет собой товар (букет цветов) в каталоге.
class Product(models.Model):
    name = models.CharField(max_length=255) # Название товара
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Цена товара
    image = models.ImageField(upload_to='products/')  # изображения товара
    description = models.TextField() # Описание товара

    def __str__(self):
        return self.name


# Модель Order представляет собой заказ, который пользователь может оформить.
class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('in_process', 'In Process'),
        ('delivered', 'Delivered')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegram_id = models.CharField(max_length=100, blank=True, null=True)  # Telegram ID пользователя
    status = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #products = models.ManyToManyField(Product)
    #status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    #delivery_address = models.CharField(max_length=255)
    #created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

# Модель Review представляет собой отзыв, который пользователь может оставить о товаре.
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    review_text = models.TextField()

    def __str__(self):
        return f"Review by {self.user.username} for {self.product.name}"