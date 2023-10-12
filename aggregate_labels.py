import json
import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyVideos.settings')
import django
django.setup()

from videos.models import Video

def unique_labels():
    videos = Video.objects.all()

    for video in videos:
        data = video.labels

        # Extract the Labels array
        labels = data.get("Labels", [])

        # Sort labels by confidence in descending order
        sorted_labels = sorted(labels, key=lambda x: x["Label"]["Confidence"], reverse=True)

        # Initialize a set to store unique labels
        unique_labels = set()

        # List of labels to exclude
        labels_to_exclude = ["Person", "Head", "Face", "Adult", "Child", "Boy", "Girl", "Male", "Female", "Man", "Woman", "Clothing"]

        # Iterate through sorted labels and add unique labels to the set
        for label in sorted_labels:
            label_name = label["Label"]["Name"]
            if label_name not in unique_labels and label_name not in labels_to_exclude:
                unique_labels.add(label_name)

            # Stop when you have 20 unique labels
            if len(unique_labels) == 20:
                break

        # Convert the set back to a list
        unique_labels_list = list(unique_labels)

        video.unique_labels = unique_labels_list
        video.save()


if __name__ == '__main__':
    unique_labels()