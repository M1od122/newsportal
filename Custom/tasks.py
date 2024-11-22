from celery import shared_task
from django.core.mail import send_mail
from .models import Subscription, Article
from django.utils import timezone
from datetime import timedelta

@shared_task
def my_job():
    one_week_ago = timezone.now() - timedelta(days=7)
    articles = Article.objects.filter(created_at__gte=one_week_ago)

    if articles.exists():
        subscriptions = Subscription.objects.all()
        for subscription in subscriptions:
            user_articles = articles.filter(category=subscription.category)
            if user_articles.exists():
                article_links = '\n'.join([f"{article.title}: http://your-site.com/articles/{article.id}/" for article in user_articles])
                send_mail(
                    'Ваш еженедельный обзор статей',
                    f'За последнюю неделю были опубликованы следующие статьи:\n{article_links}',
                    'from@example.com',
                    [subscription.user.email],
                    fail_silently=False,
                )