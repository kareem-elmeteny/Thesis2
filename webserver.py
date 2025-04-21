import os
import subprocess  # Import subprocess to manage external processes
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # Import CORS
import chromadb
import ollama
import time  # Import time module to measure execution time

# Get the absolute path of the current Python file
currentFilePath = os.path.abspath(__file__)
baseDir = os.path.dirname(currentFilePath)  # Get the directory of the current file
distFolder = os.path.join(baseDir, 'webui', 'dist')  # Join the base directory with 'webui/dist'
chromaDbPath = os.path.join(baseDir, 'chromadata')  # Path to ChromaDB data

app = Flask(__name__, static_folder=distFolder)  # Set the static folder
CORS(app)

# Configuration
chromaCollectionName = "amazonReviews"
ollamaModel = "nomic-embed-text"

# Start ChromaDB in the background
chromaProcess = subprocess.Popen(
    ["chroma", "run", "--host", "localhost", "--port", "8000", "--path", chromaDbPath],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

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
        start_time = time.time()  # Start the timer

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

        end_time = time.time()  # End the timer
        elapsed_time = end_time - start_time  # Calculate elapsed time in seconds

        return jsonify({"response": response, "time_taken": elapsed_time})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_static_files(path):
    # Serve static files from the webui/dist directory
    if path == '' or not os.path.exists(os.path.join(app.static_folder, path)):
        path = 'index.html'  # Default to index.html for SPA
    return send_from_directory(app.static_folder, path)


if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        # Terminate the ChromaDB process when the webserver exits
        print("Terminating ChromaDB process...")
        chromaProcess.terminate()
        chromaProcess.wait()