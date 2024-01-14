from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("posts/", views.ListPosts.as_view(), name="posts"),
    path("posts/<int:pk>", views.PostDetails.as_view(), name="post-details"),
    path("posts/create/", views.AddPost.as_view(), name="add_post"),
    path("posts/edit/<int:pk>", views.UpdatePost.as_view(), name="edit_post"),
    path("posts/delete/<int:pk>", views.delete_post, name="delete_post"),
    path("posts/comment/delete/<int:pk>", views.delete_comment, name="delete_comment"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
