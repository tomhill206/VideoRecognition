import boto3
from decouple import config

def create_sns_topic(topic_name):
    # Initialize the SNS client
    sns_client = boto3.client('sns',
                             aws_access_key_id=config('AWS_ACCESS_KEY_ID'),
                             aws_secret_access_key=config('AWS_SECRET_ACCESS_KEY'),
                             region_name=config('AWS_S3_REGION_NAME'))

    try:
        # Create the SNS topic
        response = sns_client.create_topic(Name=topic_name)

        # Extract the ARN of the created topic from the response
        topic_arn = response['TopicArn']

        return topic_arn

    except Exception as e:
        # Handle any errors that might occur during the process
        print("Error:", e)
        return None

# Example usage:
if __name__ == '__main__':
    # Replace 'YOUR_TOPIC_NAME' with the desired name for your SNS topic
    topic_name = 'VideoRekognitionNotification'

    # Create the SNS topic
    sns_topic_arn = create_sns_topic(topic_name)

    if sns_topic_arn:
        print("SNS Topic ARN:", sns_topic_arn)
    else:
        print("Failed to create SNS topic or encountered an error.")
