from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import chromadb
import ollama

app = Flask(__name__)
CORS(app)

# Configuration
chromaCollectionName = "amazonReviews"
ollamaModel = "nomic-embed-text"

# Initialize ChromaDB client and collection
chromaClient = chromadb.HttpClient(host="localhost", port=8000)
collection = chromaClient.get_or_create_collection(name=chromaCollectionName)

@app.route('/query', methods=['POST'])
def handle_query():
    # Parse the JSON request
    data = request.get_json()
    if not data or 'query' not in data or 'RAG' not in data:
        return jsonify({"error": "Invalid request. Must include 'query' and 'RAG'."}), 400

    query = data['query']
    use_rag = data['RAG']

    if not query:
        return jsonify({"error": "Query cannot be empty."}), 400

    # Perform the query
    try:
        if use_rag:
            # Generate embeddings for the query
            queryEmbed = ollama.embed(model=ollamaModel, input=query)['embeddings']
            
            # Retrieve related documents from ChromaDB
            relatedDocs = '\n\n'.join(collection.query(query_embeddings=queryEmbed, n_results=10)['documents'][0])
            
            # Create the RAG prompt
            prompt = f"{query} - Answer that question using the following text as a resource: {relatedDocs}"
            
            # Generate response with RAG
            ragOutput = ollama.generate(model="mistral", prompt=prompt, stream=False)
            response = ragOutput['response']
        else:
            # Generate response without RAG
            noRagOutput = ollama.generate(model="mistral", prompt=query, stream=False)
            response = noRagOutput['response']

        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)