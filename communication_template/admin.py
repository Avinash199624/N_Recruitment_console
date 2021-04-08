from django.contrib import admin
from django.contrib.admin import register
from communication_template.models import TemplateType,TemplateMaster

@register(TemplateType)
class TemplateTypeAdmin(admin.ModelAdmin):
    list_display = ['id','temp_type','is_deleted']

@register(TemplateMaster)
class TemplateMasterAdmin(admin.ModelAdmin):
    list_display = ['template_id','template_name','subject','body','type','is_active','is_deleted']