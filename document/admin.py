from django.contrib import admin
from django.contrib.admin import register
from document.models import DocumentMaster

@register(DocumentMaster)
class DocumentMasterAdmin(admin.ModelAdmin):
    list_display = ['id','doc_type','doc_name','file_size']

