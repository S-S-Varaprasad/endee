import os
from search import search
from utils.rag import generate_answer

def main():
    print("=" * 50)
    print(" Simple RAG App (Local Embeddings & LLM)")
    print("=" * 50)
    
    while True:
        query = input("\nEnter your question (or 'quit' to exit): ").strip()
        if not query:
            continue
        if query.lower() in ["quit", "exit"]:
            break
            
        print("\n[1] Searching for relevant context...")
        results = search(query, top_k=5)
        
        if not results:
            continue
            
        context = "\n".join([text for score, text in results])
        print(f"    Retrieved {len(results)} relevant chunks.")
        
        print("\n[2] Generating answer using LLM...")
        answer = generate_answer(query, context)
        
        print(f"\n--- Answer ---\n{answer}\n--------------")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    main()
