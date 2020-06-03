from django.contrib import admin
from .models import Blog, Comment, Subscribe

admin.site.register(Blog)
admin.site.register(Subscribe)
admin.site.register(Comment)


admin.site.site_header = "ArtOfCoding"
admin.site.site_title = "Adminpanel"
