from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.core.paginator import Paginator



def news_list(request):
    posts = Post.objects.filter(post_type='news').order_by('-created_at')
    paginator = Paginator(posts, 10)  # Показывать 10 новостей на странице
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_list.html', {'page_obj': page_obj})

def news_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'news_detail.html', {'post': post})

def news_search(request):
    f = PostFilter(request.GET, queryset=Post.objects.filter(post_type='news'))
    return render(request, 'news/search.html', {'filter': f})

def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.author  # или другое назначение автора
            post.post_type = 'news'  # или 'article' в зависимости от страницы
            post.save()
            return redirect('news_list')
    else:
        form = PostForm()
    return render(request, 'news/post_form.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('news_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'news/post_form.html', {'form': form})

def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('news_list')
    return render(request, 'news/post_confirm_delete.html', {'post': post})