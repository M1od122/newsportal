from django.db import models
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AbstractUser
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import User, Article, Subscription

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        self.rating = (self.post_set.aggregate(models.Sum('rating'))['rating__sum'] or 0) * 3 + \
                      self.user.comment_set.aggregate(models.Sum('rating'))['rating__sum'] or 0 + \
                      Comment.objects.filter(post__author=self).aggregate(models.Sum('rating'))['rating__sum'] or 0
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    POST_TYPE_CHOICES = (
        ('article', 'Статья'),
        ('news', 'Новость'),
    )
    post_type = models.CharField(max_length=7, choices=POST_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=250)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...' if len(self.text) > 124 else self.text


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

class UserProfile(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'profile_edit.html'
    success_url = reverse_lazy('profile')

@receiver(post_save, sender=User)
def create_user_groups(sender, instance, created, kwargs):
    if created:
        common_group, _ = Group.objects.get_or_create(name='common')
        common_group.user_set.add(instance)

from django.contrib.auth.decorators import login_required, user_passes_test

def is_author(user):
    return user.groups.filter(name='authors').exists()

@login_required
@user_passes_test(is_author)
def create_news(request):

@login_required
@user_passes_test(is_author)
def edit_news(request, pk):

group_authors = Group.objects.get(name='authors')
permission = Permission.objects.get(codename='add_post')
group_authors.permissions.add(permission)

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'category')

class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=User)
@receiver(post_save, sender=Article)
def handle_post_save(sender, instance, created, **kwargs):
    if created:
        if isinstance(instance, User):
            send_mail(
                'Добро пожаловать!',
                'Спасибо за регистрацию на нашем сайте!',
                'from@example.com',
                [instance.email],
                fail_silently=False,
            )
        elif isinstance(instance, Article):
            subscriptions = Subscription.objects.filter(category=instance.category)
            for subscription in subscriptions:
                send_mail(
                    'Новая статья в вашей подписке',
                    f'Новая статья: {instance.title}\n\nПодробнее: http://your-site.com/articles/{instance.id}/',
                    'from@example.com',
                    [subscription.user.email],
                    fail_silently=False,
                )