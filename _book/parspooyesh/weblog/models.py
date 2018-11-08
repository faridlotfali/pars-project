from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.urlresolvers import reverse

from .utils import unique_slug_generator


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    post_title = models.CharField(max_length=300)
    post_text = models.TextField(max_length=3000)
    post_img = models.FileField(upload_to='weblog', blank=True)
    created_date = models.DateTimeField(default=timezone.now)
    pub_date = models.DateTimeField('date published', blank=True, null=True)
    timestamp = models.DateField(auto_now_add = True)
    slug = models.SlugField(null = True,blank = True)
    seen = models.BigIntegerField(default = 0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.post_title

    def get_absolute_url(self):
        return reverse('weblog:detail',kwargs = {'slug' : self.slug})    

def p_pre_save_reciever(sender, instance ,*args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# def p_post_save_reciever(sender,Post0- instance ,created ,*args, **kwargs):
#     if not instance.slug:
#         instance.slug = unique_slug_generator(instance)

pre_save.connect(p_pre_save_reciever, sender = Post)    
# post_save.connect(p_post_save_reciever, sender = Post)    

class slider(models.Model):
    image = models.ForeignKey('post', on_delete=models.CASCADE)
        


class Comment(models.Model):
    comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=200)
    votes =  models.IntegerField(default=0)

    def __str__(self):
        return self.comment_text

    def get_absolute_url(self):
        return reverse('weblog:detail',kwargs = {'slug' : self.comment.slug})    


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    email_confirmed = models.BooleanField(default=False)
    
    def __str__(self):  # __unicode__ for Python 2
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

# class SiteSetting(models.Model):
#     setting_name =  models.CharField(max_length=50, blank=False)
#     apply = models.BooleanField(default = False)

#     def save(self, *args, **kwargs):
#         if self.apply:
#             print(super(SiteSetting, self).objects.all)    
#         super(SiteSetting, self).save(*args, **kwargs)

# class links(models.Model):
#     site = models.ForeignKey(SiteSetting , on_delete = models.CASCADE )
#     link_name =  models.CharField(max_length=100, blank=False)
#     link =  models.TextField(max_length=500, blank=False)

#     def __str__(self):
#         return self.link_name 

class SiteSettings(models.Model):
    key_name = models.CharField(max_length=50)    
    key_value = models.TextField(max_length=500)    

    def __str__(self):
        return self.key_name
