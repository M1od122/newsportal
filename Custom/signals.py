from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Article

@receiver(post_save, sender=Article)
def send_article_notification(sender, instance, created, kwargs, notify_subscribers=None):
    """Отправка уведомления при создании новой статьи."""
    if created:
        notify_subscribers.delay(instance)