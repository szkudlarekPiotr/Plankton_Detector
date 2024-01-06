from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=500)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    date_pub = models.DateField(auto_now_add=True)

    @property
    def sorted_comments(self):
        return self.comment_set.all().order_by("-date_added")


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_added = models.DateField(auto_now_add=True)
