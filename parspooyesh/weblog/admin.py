from django.contrib import admin

# Register your models here.
from .models import Comment
from .models import Post

admin.site.register(Post)
admin.site.register(Comment)