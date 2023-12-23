from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("posts/", views.ListPosts.as_view(), name="posts"),
    path("posts/<int:pk>", views.PostDetails.as_view(), name="post-details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)