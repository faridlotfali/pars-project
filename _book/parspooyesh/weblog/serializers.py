from rest_framework import serializers
from django.contrib.auth.models import User 
from .models  import *

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author', 'post_title', 'post_text')

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'token'
        ]