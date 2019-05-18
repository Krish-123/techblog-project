from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.contrib.auth import get_user_model

# Create your models here.

class PostModel(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey('auth.user',on_delete=models.CASCADE)
    post = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True,null=True)
    likes = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def approved_comments(self):
        return self.comments.filter(approved=True)
    def get_absolute_url(self):
        return reverse('blog:post_detail',kwargs={'pk':self.pk})

class CommentModel(models.Model):
    author = models.CharField(max_length=256)
    comment = models.TextField()
    commented_date = models.DateTimeField(default=timezone.now)
    approved = models.BooleanField(default=False)
    post = models.ForeignKey(PostModel,related_name='comments',on_delete=models.CASCADE)

    def __str__(self):
        return self.comment

    def approve(self):
        self.approved = True
        self.save()
    
    def get_absolute_url(self):
        return reverse('blog:index')