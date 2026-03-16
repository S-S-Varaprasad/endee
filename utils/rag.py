from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load a small local LLM for generation
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("google/flan-t5-small")

def generate_answer(query: str, context: str) -> str:
    """Generates an answer to the query using the provided context."""
    prompt = f"Answer the following question based only on the provided context.\n\nContext:\n{context}\n\nQuestion:\n{query}\n\nAnswer:"
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_new_tokens=150)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
