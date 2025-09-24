from django.urls import path
from .views import UploadFileView, AskQuestionView

urlpatterns = [
    path("upload/", UploadFileView.as_view(), name="upload-file"),
    path("ask/", AskQuestionView.as_view(), name="ask-question"),
]
