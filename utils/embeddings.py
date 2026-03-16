from sentence_transformers import SentenceTransformer

# Load a small, fast local model for embeddings
model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str) -> list[float]:
    """Generates a vector embedding for the given text."""
    return model.encode(text).tolist()
