from django.db import models
class Video(models.Model):
    title = models.CharField(max_length=100)
    labels = models.JSONField(null=True)
    video_file = models.URLField()
    thumbnail_file = models.URLField()

    def __str__(self):
        return self.title