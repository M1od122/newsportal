import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author__user__username': ['icontains'],
            'created_at': ['gte'],
        }