from transformers import BertTokenizer, BertModel
import torch

model_name = "bert-base-uncased"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertModel.from_pretrained(model_name)

labels = ['Laughing', 'Wedding', 'Baby Laughing', 'Crawling', 'Baby', 'Portrait', 'Romantic', 'Indoors', 'Hugging', 'Jacket', 'Coat', 'Interior Design', 'Kissing', 'Bride', 'Happy', 'Floor', 'Wood', 'People', 'Smoke', 'Photography']  # Your list of 300 labels

# Tokenize the labels and convert them to tensors
inputs = tokenizer(labels, return_tensors="pt", padding=True, truncation=True, max_length=32)

# Forward pass through the model
with torch.no_grad():
    outputs = model(**inputs)

# Get the embeddings from the model output
embeddings = outputs.last_hidden_state.mean(dim=1)  # You can also use other pooling strategies, like max pooling

print(embeddings)
