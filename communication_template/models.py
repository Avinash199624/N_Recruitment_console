from django.db import models
import uuid
from django.db.models import Q, UniqueConstraint
from user.models import BaseModel

class TemplateType(BaseModel):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    temp_type = models.CharField(max_length=100,null=True,blank=True)
    is_deleted = models.BooleanField(default=False,help_text="Used for Soft Delete")

    def __str__(self):
        return self.temp_type

class TemplateMaster(BaseModel):

    template_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    template_name = models.CharField(max_length=100,null=True,blank=True)
    subject = models.CharField(max_length=200,null=True,blank=True)
    body = models.TextField(blank=True, null=True)
    type = models.ForeignKey('TemplateType',null=True, blank=True, on_delete=models.SET_NULL,
                                   related_name="template_type")
    is_active = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False, help_text="Used for Soft Delete")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["type", "is_active"],condition=Q(is_active=True), name='unique_level_per_type'),
        ]

    def __str__(self):
        return ' '.join([self.template_name,self.type.temp_type])