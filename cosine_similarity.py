import torch
from sklearn.metrics.pairwise import cosine_similarity
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyVideos.settings')
import django
django.setup()

from videos.models import Video
videos = Video.objects.all()

import ast

# Extract video embeddings and convert to PyTorch tensors
video_embeddings = [ast.literal_eval(video.embeddings)[0] for video in videos]


# Load another tensor that you want to compare with video embeddings
# For example, let's assume you have another tensor 'other_tensor'
other_tensor = video_embeddings[0]

#breakpoint()

# Calculate the cosine similarity between video embeddings and other_tensor
# The result will be a list of cosine similarity scores
cosine_scores = cosine_similarity(video_embeddings, [other_tensor])

# Sort video IDs based on cosine similarity scores
video_ids = [video.id for video in videos]  # Assuming each video object has an "id" field
sorted_video_ids = [id for _, id in sorted(zip(cosine_scores, video_ids), reverse=True)]

# Get the top 10 video IDs with the highest similarity
top_10_similarity_video_ids = sorted_video_ids[:10]

print("Top 10 similar video IDs:", top_10_similarity_video_ids)
