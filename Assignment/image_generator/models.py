from django.db import models

class ImageMetadata(models.Model):
    text_prompt = models.CharField(max_length=255)
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True)