import os
from flask import Flask, render_template, request, jsonify
from search import search
from utils.rag import generate_answer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "Empty query"}), 400

    results = search(query, top_k=5)
    if not results:
        return jsonify({"answer": "I couldn't find any relevant context to answer your question."})
        
    context = "\n".join([text for score, text in results])
    answer = generate_answer(query, context)
    
    return jsonify({"answer": answer, "context_chunks": len(results)})

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    app.run(host="127.0.0.1", port=5000, debug=True)
