from django.contrib import admin

# Register your models here.
from .models import Comment,slider
from .models import Post

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(slider)