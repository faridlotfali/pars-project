from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class question(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    
    def __str__(self):
        return self.text

class option(models.Model):
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    text = models.TextField(max_length=3000)
    votes =  models.IntegerField(default=0)

    def __str__(self):
        return self.text
