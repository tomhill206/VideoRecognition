from transformers import BertTokenizer, BertModel
import torch
import ast
import os 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FamilyVideos.settings')
import django
django.setup()

from videos.models import Video

model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

# Function to generate embeddings for a list of labels using BERT
def generate_embeddings_for_labels(labels, tokenizer, model):
    # Join the labels list into a single string
    labels_text = " ".join(labels)
    
    # Tokenize and encode the labels using BERT
    inputs = tokenizer(labels_text, return_tensors="pt", padding=True, truncation=True, max_length=40)
    
    # Get BERT embeddings for the labels
    with torch.no_grad():
        outputs = model(**inputs)
    
    # Extract the embeddings for the [CLS] token (the first token)
    embeddings = outputs.last_hidden_state.mean(dim=1)
    
    return embeddings

videos = Video.objects.all()

# Iterate through video objects and add embeddings to the 'embeddings' field
for video in videos:
    unique_labels_text = video.unique_labels
    
    # Parse the labels text and convert it into a list
    unique_labels = ast.literal_eval(unique_labels_text)
    
    # Generate embeddings for unique labels
    label_embeddings = generate_embeddings_for_labels(unique_labels, tokenizer, model)
    
    # Add the embeddings tensor to the video object
    video.embeddings = label_embeddings.tolist()

    video.save()


