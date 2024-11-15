"""
URL configuration for NewsPortal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import news_list, news_detail, news_search, post_create, post_edit, post_delete


urlpatterns = [
    path('news/', news_list, name='news_list'),
    path('news/search/', news_search, name='news_search'),
    path('news/create/', post_create, name='post_create'),
    path('news/<int:pk>/edit/', post_edit, name='post_edit'),
    path('news/<int:pk>/delete/', post_delete, name='post_delete')
    path('news/<int:post_id>/', news_detail, name='news_detail'),
    path('admin/', admin.site.urls),
    path('pages/', include('django.contrib.flatpages.urls')),
    path('accounts/login/', allauth_views.LoginView.as_view(), name='account_login'),
    path('accounts/signup/', allauth_views.SignupView.as_view(), name='account_signup'),
    path('accounts/yandex/login/', allauth_views.YandexOAuth2Adapter.as_view(), name='yandex_login'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
]
