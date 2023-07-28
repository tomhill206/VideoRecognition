import boto3
from decouple import config

def analyze_video_from_s3(bucket_name, video_key):
    # Initialize the Rekognition client
    rekognition_client = boto3.client('rekognition',
                             aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                             region_name=config('AWS_S3_REGION_NAME'))

    # Specify the S3 bucket and video file
    video_s3_object = {'Bucket': bucket_name, 'Name': video_key}

    # Specify the desired features for analysis
    # In this example, we use label detection
    # You can modify the list of features based on your requirements.
    features = ['LABELS']

    try:
        # Start the video analysis
        response = rekognition_client.start_label_detection(
            Video={'S3Object': video_s3_object},
            NotificationChannel={
                'SNSTopicArn': config('AWS_SNSTOPICARN'),  # Replace with your SNS topic ARN
                'RoleArn': config('AWS_ROLE_ARN')  # Replace with your IAM role ARN
            },
            # Optional settings: Change values as needed
            MinConfidence=50.0,  # Minimum confidence level for detected labels
            JobTag='VideoAnalysisJob'  # A unique job identifier (can be any string)
        )

        # Get the unique identifier for the video analysis job
        job_id = response['JobId']

        # Return the job ID to handle SNS notification separately
        return job_id

    except Exception as e:
        # Handle any errors that might occur during the process
        print("Error:", e)
        return None

def handle_sns_notification(job_id):
    # Initialize the Rekognition client
    rekognition_client = boto3.client('rekognition',
                             aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                             region_name=config('AWS_S3_REGION_NAME'))

    try:
        # Wait for the video analysis job to complete by receiving SNS notifications
        # Implement your logic here to receive and handle SNS notifications
        # You can use a separate function to process the results once the job is complete
        # For simplicity, we'll poll for the job status here until it's complete
        while True:
            analysis_result = rekognition_client.get_label_detection(JobId=job_id)
            if analysis_result['JobStatus'] == 'SUCCEEDED':
                return analysis_result
            elif analysis_result['JobStatus'] == 'FAILED' or analysis_result['JobStatus'] == 'STOPPED':
                print("Video analysis failed or encountered an error.")
                return None

    except Exception as e:
        print("Error:", e)
        return None

# Example usage:
if __name__ == '__main__':
    # Replace 'YOUR_BUCKET_NAME' and 'YOUR_VIDEO_KEY' with your S3 bucket and video file key
    job_id = analyze_video_from_s3(bucket_name='video-archive-video-files', video_key='1998-02-14-19_13.mp4')

    if job_id:
        print("Video analysis started. Wait for SNS notification for results.")
        response_json = handle_sns_notification(job_id)
        if response_json:
            print(response_json)
        else:
            print("Video analysis failed or encountered an error.")
    else:
        print("Video analysis failed to start or encountered an error.")
