from django.db import models
from django.core.validators import FileExtensionValidator
class UploadedFile(models.Model):
    name = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    content = models.FileField(null=True, upload_to='files/%y', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'xlsx', 'xls'])])
    def __str__(self):
        return self.name
