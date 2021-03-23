from django.contrib import admin
from .models import Blog, Comment, Subscribe, Category

admin.site.register(Blog)
admin.site.register(Subscribe)
admin.site.register(Comment)
admin.site.register(Category)


admin.site.site_header = "Knowledge Yard"
admin.site.site_title = "Admin Panel"