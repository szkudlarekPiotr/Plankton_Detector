from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post, Comment

# Create your views here.


class ListPosts(ListView):
    model = Post
    template_name = "list_posts.html"


class PostDetails(DetailView):
    model = Post
