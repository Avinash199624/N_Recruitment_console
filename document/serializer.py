from rest_framework import serializers
from document.models import DocumentMaster, InformationMaster, NewDocumentMaster


class DocumentMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentMaster
        fields = (
            "doc_id",
            "doc_name",
            "description",
        )

class NewDocumentMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewDocumentMaster
        fields = (
            "doc_id",
            "doc_name",
            "doc_type",
        )

class InformationMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = InformationMaster
        fields = (
            "info_id",
            "info_name",
            "info_type",
        )
