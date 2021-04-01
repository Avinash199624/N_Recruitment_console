from user.models import User,UserProfile,Location,UserRoles
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from drf_writable_nested import WritableNestedModelSerializer
import json
from document.models import DocumentMaster

class DocumentMasterSerializer(serializers.ModelSerializer):

    class Meta:
        model = DocumentMaster
        fields = "__all__"