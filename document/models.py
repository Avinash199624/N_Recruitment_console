from django.db import models
import uuid
from user.models import BaseModel

class DocumentMaster(BaseModel):
    doc_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doc_name = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.doc_id)

CASTE = 'caste'
PERSONAL = 'personal'
QUALIFICATION = 'qualification'
EXPERIENCE = 'experience'
PUBLISHED_PAPERS = 'published papers'
OTHERS = 'others'

DOC_TYPE_CHOICES = [
    (CASTE, 'CASTE'),
    (PERSONAL, 'PERSONAL'),
    (QUALIFICATION, 'QUALIFICATION'),
    (EXPERIENCE, 'EXPERIENCE'),
    (PUBLISHED_PAPERS, 'PUBLISHED_PAPERS'),
    (OTHERS, 'OTHERS'),
]

class NewDocumentMaster(BaseModel):
    doc_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doc_name = models.CharField(max_length=50, null=True, blank=True)
    doc_type = models.CharField(max_length=30, choices=DOC_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.doc_type



CASTE = 'caste'
PERSONAL = 'personal'
QUALIFICATION = 'qualification'
EXPERIENCE = 'experience'
PUBLISHED_PAPERS = 'published papers'
OTHERS = 'others'

INFO_TYPE_CHOICES = [
    (CASTE, 'CASTE'),
    (PERSONAL, 'PERSONAL'),
    (QUALIFICATION, 'QUALIFICATION'),
    (EXPERIENCE, 'EXPERIENCE'),
    (PUBLISHED_PAPERS, 'PUBLISHED_PAPERS'),
    (OTHERS, 'OTHERS'),
]

class InformationMaster(BaseModel):
    info_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    info_name = models.CharField(max_length=50, null=True, blank=True)
    info_type = models.CharField(max_length=30, choices=INFO_TYPE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.info_type
