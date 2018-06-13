from django.db import models
from django.utils import timezone

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post_title = models.CharField(max_length=300)
    post_text = models.TextField(max_length=3000)
    created_date = models.DateTimeField(default=timezone.now)
    pub_date = models.DateTimeField('date published', blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.post_title



class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    votes =  models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text