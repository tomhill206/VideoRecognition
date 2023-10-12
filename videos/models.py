from django.db import models
class Video(models.Model):
    title = models.CharField(max_length=100)

    labels = models.JSONField(null=True)

    date_time = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    duration = models.IntegerField(null=True)

    video_file = models.CharField(max_length=100)
    thumbnail_file = models.CharField(max_length=100)

    unique_labels = models.TextField(blank=True)
    embeddings = models.TextField(blank=True)

    def __str__(self):
        return self.title