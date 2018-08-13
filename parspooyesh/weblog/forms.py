from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Post,Comment

class SignUpForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'password1', 'password2', )

class SignUpForm2(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', )        

class site_settings(forms.Form):
    key_name = forms.CharField(max_length=50)
    key_value= forms.CharField(max_length=500)

class PostForm(forms.ModelForm):
    class Meta:
        model  = Post
        fields =[
            'post_title',
            'post_text',
            'post_img'
        ]

class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields =[
            'comment_text',
        ]       