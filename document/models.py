from django.db import models
import uuid

class DocumentMaster(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doc_type = models.CharField(max_length=50, null=True, blank=True)
    doc_name = models.CharField(max_length=50, null=True, blank=True)
    file_size = models.IntegerField(null=True, blank=True,help_text="Document file size in MB")
    is_deleted = models.BooleanField(default=False,help_text="Used for Soft Delete")

    def __str__(self):
        return ' '.join([self.doc_type,self.doc_name])