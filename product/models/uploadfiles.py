from django.db import models


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
