from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import urls

urlpatterns = [
    path("", views.DetectView.as_view(), name="detect"),
    path("history/", views.ListHistory.as_view(), name="history"),
    path(
        "detection/<int:pk>", views.DetectionDetails.as_view(), name="detection-details"
    ),
    path("export_pred/<int:pk>", views.download_pred, name="download_predictions"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
