import boto3
import django
from django.shortcuts import render
from .models import Video
from django.contrib.auth.decorators import login_required
from django.conf import settings

import torch
from sklearn.metrics.pairwise import cosine_similarity
import os
import ast
from transformers import BertTokenizer, BertModel

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyVideos.settings')
django.setup()

@login_required
def video_list(request):
    videos = Video.objects.all()
    for video in videos:
        video.signed_url = generate_signed_url('video-archive-video-files', video.video_file)
        video.thumbnail_signed_url = generate_signed_url('video-archive-thumbnail-files', video.thumbnail_file)

    #breakpoint()
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

def search(request):
    query = request.GET.get('query', '')  # Get the query from the URL parameter
    
    #breakpoint()
    videos = generate_results(query)

    for video in videos:
        video.signed_url = generate_signed_url('video-archive-video-files', video.video_file)
        video.thumbnail_signed_url = generate_signed_url('video-archive-thumbnail-files', video.thumbnail_file)

    return render(request, 'search_results.html', {'videos': videos, 'query': query})

def generate_results(query):
    videos = Video.objects.all()

    # Extract video embeddings and convert to PyTorch tensors
    video_embeddings = [ast.literal_eval(video.embeddings)[0] for video in videos]

    query_embedding = get_embedding(query)

    # Calculate the cosine similarity between video embeddings and other_tensor
    # The result will be a list of cosine similarity scores
    cosine_scores = cosine_similarity(video_embeddings, [query_embedding])

    sorted_videos = [video for _, video in sorted(zip(cosine_scores, videos), reverse=True)]

    # Get the top 10 video IDs with the highest similarity
    top_similarity_videos = sorted_videos[:20]

    return top_similarity_videos
    
def get_embedding(content):

    model_name = "bert-base-uncased"
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertModel.from_pretrained(model_name)
    # Tokenize and encode the labels using BERT
    inputs = tokenizer(content, return_tensors="pt", padding=True, truncation=True, max_length=40)
    
    # Get BERT embeddings for the labels
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Extract the embeddings for the [CLS] token (the first token)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    
    return embeddings.tolist()[0]
