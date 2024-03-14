from typing import Any
from django.db.models.query import QuerySet
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, FormMixin, UpdateView
from .models import Post, Comment
from .froms import PostForm, CommentForm


class ListPosts(ListView):
    model = Post
    template_name = "list_posts.html"
    paginate_by = 3

    def get_queryset(self) -> QuerySet[Any]:
        queryset = Post.objects.all().order_by("-date_pub")
        return queryset


class PostDetails(DetailView, FormMixin):
    model = Post
    template_name = "post_details.html"
    form_class = CommentForm

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form) -> HttpResponse:
        post = self.get_object()
        new_comment = form.save(commit=False)
        new_comment.author = self.request.user
        new_comment.post = post
        new_comment.save()
        return redirect("post-details", pk=post.id)


class AddPost(FormView):
    template_name = "add_post.html"
    form_class = PostForm

    def form_valid(self, form) -> HttpResponse:
        new_post = form.save(commit=False)
        new_post.author = self.request.user
        new_post.save()
        return redirect("post-details", pk=new_post.id)


class UpdatePost(UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = "add_post.html"

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        post = form.save()
        return redirect("post-details", pk=post.id)


def delete_post(request, pk):
    object = Post.objects.get(pk=pk)
    object.delete()
    return redirect("posts")


def delete_comment(request, pk):
    object = Comment.objects.get(pk=pk)
    post = object.post
    object.delete()
    return redirect("post-details", pk=post.id)
