from django.db import models

class Post(models.Model):
    post_title = models.CharField(max_length=300)
    post_text = models.TextField(max_length=3000)
    pub_date = models.DateTimeField('date published')


class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    votes =  models.IntegerField(default=0)