from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import datetime

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    joined = models.DateTimeField(default=now)
    image = models.ImageField(default="default/user.png", upload_to='images')
    bio = models.TextField(default=None, blank=True, null=True)
    savepost = []

    def post_count(self):
        return Post.objects.filter(user=self.user).count()
    
    def reply_count(self):
        return Replie.objects.filter(user=self.user).count()
    
    def doj(self):
        return datetime.strftime(self.joined, "%B, %Y")
    
    def save_post(self, data):
        return self.savepost.append(data)
    
    def remove_post(self, data):
        return self.savepost.remove(data)
    
    def get_saved_post(self):
        return self.savepost
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post_id = models.AutoField
    post_content = models.CharField(max_length=5000)
    timestamp= models.DateTimeField(default=now)
    image = models.ImageField(upload_to="images",default="")

class Replie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    reply_id = models.AutoField
    reply_content = models.CharField(max_length=5000) 
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default='')
    timestamp= models.DateTimeField(default=now)
    image = models.ImageField(upload_to="images",default="")
    