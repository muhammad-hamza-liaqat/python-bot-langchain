from django.urls import path
from .views import UploadDocumentView, QueryDocumentView

urlpatterns = [
    path("upload/", UploadDocumentView.as_view(), name="upload-document"),
    path("query/", QueryDocumentView.as_view(), name="query-document"),
]
