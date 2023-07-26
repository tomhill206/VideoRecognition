import boto3
from django.shortcuts import render
from .models import Video
from django.contrib.auth.decorators import login_required
from django.conf import settings

@login_required
def video_list(request):
    videos = Video.objects.all()
    for video in videos:
        video.signed_url = generate_signed_url('video_archive_video_files', video.video_url)
        video.thumbnail_signed_url = generate_signed_url('video_archive_thumbnail_files', video.thumbnail_url)
    return render(request, 'video_list.html', {'videos': videos})

    
def generate_signed_url(bucket_name, object_key):
    s3_client = boto3.client('s3',
                             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                             region_name=settings.AWS_S3_REGION_NAME)
    signed_url = s3_client.generate_presigned_url('get_object',
                                                  Params={'Bucket': bucket_name,
                                                          'Key': object_key},
                                                  ExpiresIn=settings.SIGNED_URL_EXPIRATION_TIME)
    return signed_url