from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=500)
    content = RichTextField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_pub = models.DateTimeField(auto_now_add=True)

    @property
    def sorted_comments(self):
        return self.comment_set.all().order_by("-date_added")


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
