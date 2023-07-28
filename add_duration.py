import os
import boto3
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyVideos.settings')
import django
django.setup()

from videos.models import Video

def add_duration():
    videos = Video.objects.all()

    for video in videos:
        video.duration = video.labels['VideoMetadata']['DurationMillis']
        video.save()

if __name__ == '__main__':
    add_duration()