from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Order
from ZeroCoder.shop.bot import notify_admin  # Импорт функции для уведомления администратора

@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        notify_admin(instance)  # Уведомление администратора о новом заказе