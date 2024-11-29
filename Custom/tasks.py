from celery import shared_task
from django.core.mail import send_mail
from .models import Subscription, Article
from django.utils import timezone
from datetime import timedelta

@shared_task
def notify_subscribers(article_instance):
    """Отправка уведомления подписчикам о новой статье."""
    subscriptions = Subscription.objects.filter(category=article_instance.category)
    for subscription in subscriptions:
        send_mail(
            'Новая статья в вашей подписке',
            f'Новая статья: {article_instance.title}\n\nПодробнее: http://site.com/articles/{article_instance.id}/',
            'from@example.com',
            [subscription.user.email],
            fail_silently=False,
        )

@shared_task
def my_job():
    """Еженедельная рассылка уведомлений о новых статьях."""
    one_week_ago = timezone.now() - timedelta(days=7)
    articles = Article.objects.filter(created_at__gte=one_week_ago)

    if articles.exists():
        subscriptions = Subscription.objects.all()
        for subscription in subscriptions:
            user_articles = articles.filter(category=subscription.category)
            if user_articles.exists():
                article_links = '\n'.join([f"{article.title}: http://site.com/articles/{article.id}/" for article in user_articles])
                send_mail(
                    'Ваш еженедельный обзор статей',
                    f'За последнюю неделю были опубликованы следующие статьи:\n{article_links}',
                    'from@example.com',
                    [subscription.user.email],
                    fail_silently=False,
                )