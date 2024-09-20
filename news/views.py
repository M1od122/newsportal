from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    news_posts = Post.objects.filter(post_type='news').order_by('-created_at')
    return render(request, 'news_list.html', {'news_posts': news_posts})

def news_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'news_detail.html', {'post': post})