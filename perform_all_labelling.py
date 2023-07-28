import boto3
import django
from decouple import config
from utils.call_API import analyze_video_from_s3, handle_sns_notification
from django.core.exceptions import ObjectDoesNotExist
import os
import django

# Set the environment variable for Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyVideos.settings')

# Initialize Django
django.setup()

from videos.models import Video

def update_labels_in_database(video, labels):
    try:
        # Update the 'labels' field for the Video object
        video.labels = labels

        # Save the changes to the database
        video.save()

        print(f"Labels updated in the database for video titled {title}.")

    except ObjectDoesNotExist:
        print(f"video titled {title} does not exist.")
    except Exception as e:
        print(f"Error updating labels for video titled {title}: {e}")

# Example usage:
if __name__ == '__main__':
    videos = Video.objects.all()
    bucket_name = "video-archive-video-files"  # Replace with the actual bucket name for the video

    for video in videos:
        
        job_id = analyze_video_from_s3(bucket_name=bucket_name, video_key=video.video_file)

        title = video.title

        if job_id:
            print(f"Video analysis started for video titled {title}. Wait for SNS notification for results.")
            response_json = handle_sns_notification(job_id)
            if response_json:

                # Update the 'labels' field in the database for the video with the given video_id
                update_labels_in_database(video, response_json)
                print(f"Labels updated in the database for video titled {title}.")
            else:
                print(f"Video analysis failed or encountered an error for video titled {title}.")
        else:
            print(f"Video analysis failed to start or encountered an error for video titled {title}.")