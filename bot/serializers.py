from rest_framework import serializers

class UploadFileSerializer(serializers.Serializer):
    file = serializers.FileField()

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=500)
