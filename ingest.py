import os
import time
from utils.embeddings import get_embedding
from endee import Endee, Precision

DATA_FILE = "data/java_notes.txt"
ENDEE_URL = "http://localhost:8080/api/v1"
INDEX_NAME = "java_notes_index"

def main():
    print(f"Reading data from {DATA_FILE}...")
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        text = f.read()
    
    # Simple chunking: split by lines
    chunks = [line.strip() for line in text.split("\n") if line.strip()]
    
    print(f"Connecting to Endee at {ENDEE_URL}...")
    client = Endee()
    client.set_base_url(ENDEE_URL)
    
    print(f"Creating/getting index '{INDEX_NAME}'...")
    try:
        index = client.get_index(name=INDEX_NAME)
        print("Index found.")
    except Exception:
        print("Index not found. Creating new index...")
        # 384 dimensions for all-MiniLM-L6-v2
        client.create_index(
            name=INDEX_NAME,
            dimension=384,
            space_type="cosine",
            precision=Precision.FLOAT32,
        )
        # Give it a moment to initialize
        time.sleep(1)
        index = client.get_index(name=INDEX_NAME)
        print("Index created.")

    print(f"Found {len(chunks)} chunks. Generating embeddings & Upserting to Endee...")
    
    items = []
    # Using enumerate as ID (converted to string)
    for i, chunk in enumerate(chunks):
        vec = get_embedding(chunk)
        items.append({
            "id": f"chunk_{i}",
            "vector": vec,
            "meta": {"text": chunk}
        })
        
    print(f"Upserting {len(items)} items...")
    index.upsert(items)
        
    print("Ingestion complete!")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
