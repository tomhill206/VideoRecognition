from django.db import models
class Video(models.Model):
    title = models.CharField(max_length=100)

    labels = models.JSONField(null=True)

    date_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    duration = models.DurationField(null=True)

    video_file = models.CharField(max_length=100)
    thumbnail_file = models.CharField(max_length=100)

    def __str__(self):
        return self.title