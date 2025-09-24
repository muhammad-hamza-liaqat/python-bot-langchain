from django.contrib import admin
from .models import UploadedDocument

@admin.register(UploadedDocument)
class UploadedDocumentAdmin(admin.ModelAdmin):
    list_display = ('id', 'file', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('file',)
