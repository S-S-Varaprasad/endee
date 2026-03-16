import os
from utils.embeddings import get_embedding
from endee import Endee

ENDEE_URL = "http://localhost:8080/api/v1"
INDEX_NAME = "java_notes_index"

def search(query: str, top_k: int = 2) -> list[tuple[float, str]]:
    """Searches the Endee vector store for the closest chunks to the query."""
    
    client = Endee()
    client.set_base_url(ENDEE_URL)
    
    try:
        index = client.get_index(name=INDEX_NAME)
    except Exception as e:
        print(f"Error connecting to Endee index. Is the server running? {e}")
        print("Please run docker-compose up -d and ingest.py first.")
        return []

    query_vec = get_embedding(query)
    
    try:
        results = index.query(
            vector=query_vec,
            top_k=top_k
        )
    except Exception as e:
        print(f"Error querying Endee: {e}")
        return []
        
    formatted_results = []
    for r in results:
        # Endee returns objects with id, similarity, and meta attributes
        # Based on how we ingested, meta has a "text" key
        val = r.meta if hasattr(r, 'meta') else r.get("meta", {})
        text = val.get("text", "") if hasattr(val, 'get') else str(val)
        sim = r.similarity if hasattr(r, 'similarity') else r.get("similarity", 0.0)
        formatted_results.append((float(sim), text))

    return formatted_results

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    test_query = "What is Java?"
    print(f"Searching for: '{test_query}' in Endee...")
    res = search(test_query)
    for score, text in res:
        print(f"[{score:.4f}] {text}")
