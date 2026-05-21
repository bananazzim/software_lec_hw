from django.db import models
import os


class Post(models.Model):

    title = models.CharField(max_length=200)

    content = models.TextField()

    head_image = models.ImageField(
        upload_to='blog/images/%Y/%m/%d/',
        blank=True
     )

    file_upload = models.FileField(
        upload_to='blog/files/%Y/%m/%d/',
        blank=True
     )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_file_name(self):

        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):

        return self.get_file_name().split('.')[-1]