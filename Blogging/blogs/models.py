from django.db import models
from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField


class Category(models.Model):
    category_name = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.category_name


class Blog(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default='', null=True)
    # description = models.TextField(null=True, blank=True)
    description = RichTextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog-images')
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(null=False, default='', primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment from {self.user}"

class Subscribe(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email
