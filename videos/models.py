from django.db import models
class Video(models.Model):
    title = models.CharField(max_length=100)

    labels = models.JSONField(null=True)

    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    duration = models.DurationField(null=True)

    video_file = models.CharField(max_length=100)
    video_url = models.URLField(null=True)

    thumbnail_file = models.CharField(max_length=100)
    thumbnail_url = models.URLField(null=True)

    signed_url = models.URLField(blank=True, null=True)
    thumbnail_signed_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title