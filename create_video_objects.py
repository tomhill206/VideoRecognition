import os
import boto3
from decouple import config

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyVideos.settings')
import django
django.setup()

from videos.models import Video

def create_video_objects():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY')
    )

    # Fetch the list of video files from the "video-archive-video-files" bucket
    video_files_response = s3_client.list_objects_v2(Bucket='video-archive-video-files')

    if 'Contents' in video_files_response:
        video_files = [obj['Key'] for obj in video_files_response['Contents']]

        #breakpoint()

        for video_file in video_files:
            # Construct the video URL
            video_url = f'https://video-archive-video-files.s3.eu-west-2.amazonaws.com/{video_file}'

            # Construct the thumbnail URL based on the video file name
            video_file_name = os.path.basename(video_file)
            thumbnail_file = f'{os.path.splitext(video_file_name)[0]}_thumbnail.jpg'
            thumbnail_url = f'https://video-archive-thumbnail-files.s3.eu-west-2.amazonaws.com/{thumbnail_file}'

            # Create the Video object if it doesn't already exist
            video, created = Video.objects.get_or_create(video_file=video_file, defaults={
                'title': video_file_name ,
                'video_file': video_file_name,
                'thumbnail_file': thumbnail_file,
                'video_url': video_url,
                'thumbnail_url': thumbnail_url
            })


if __name__ == '__main__':
    create_video_objects()
