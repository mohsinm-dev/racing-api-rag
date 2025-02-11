# app/utils/embedding.py
from app.core.logging import logger
from sentence_transformers import SentenceTransformer

# Load the pre-trained Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

def generate_embedding(text: str) -> list:
    try:
        # Generate the embedding for the input text
        embedding = model.encode(text)
        return embedding.tolist()  # Convert to list for consistency
    except Exception as e:
        logger.error("Error generating embedding: %s", e)
        return []
