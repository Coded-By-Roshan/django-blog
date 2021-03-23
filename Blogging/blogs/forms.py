from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import  forms
from .models import Blog


class Userregister(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class BlogForm(forms.ModelForm):
    
    class Meta:
        model = Blog
        fields = '__all__'
        exclude = ['views','likes','user']