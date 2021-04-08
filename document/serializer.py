from rest_framework import serializers
from document.models import DocumentMaster

class DocumentMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentMaster
        fields = (
            "id",
            "doc_type",
            "doc_name",
            "file_size",
        )