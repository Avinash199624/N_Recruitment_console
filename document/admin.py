from django.contrib import admin
from django.contrib.admin import register
from document.models import DocumentMaster

@register(DocumentMaster)
class DocumentMasterAdmin(admin.ModelAdmin):
    list_display = ['doc_id','doc_name','description', 'is_deleted']

