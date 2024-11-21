from django import forms
from .models import Subscription, Category

from NewsPortal.news.models import UserProfile
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'categories']

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['username', 'first_name', 'last_name', 'email', 'avatar', 'bio']  # Укажите нужные поля

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError("Этот адрес электронной почты уже занят.")
        return email

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = ['category']
        widgets = {
            'category': forms.CheckboxSelectMultiple,
        }