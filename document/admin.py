from django.contrib import admin
from django.contrib.admin import register
from document.models import DocumentMaster, NewDocumentMaster, InformationMaster

@register(DocumentMaster)
class DocumentMasterAdmin(admin.ModelAdmin):
    list_display = ['doc_id', 'doc_name', 'description', 'is_deleted']


@register(NewDocumentMaster)
class NewDocumentMasterAdmin(admin.ModelAdmin):
    list_display = ['doc_id', 'doc_name', 'doc_type', 'is_deleted']


@register(InformationMaster)
class InformationMasterAdmin(admin.ModelAdmin):
    list_display = ['info_id', 'info_name', 'info_type', 'is_deleted']

