from rest_framework import serializers
from .models import UploadedDocument

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedDocument
        fields = ['id', 'file', 'uploaded_at']
