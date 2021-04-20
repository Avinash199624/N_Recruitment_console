from rest_framework import serializers
from document.models import DocumentMaster

class DocumentMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentMaster
        fields = (
            "doc_id",
            "doc_name",
            "description",
        )