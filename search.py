import os
import subprocess
import sys, chromadb, ollama

chromaCollectionName = "amazonReviews"
ollamaModel = "nomic-embed-text"
# Get the absolute path of the current Python file
currentFilePath = os.path.abspath(__file__)
baseDir = os.path.dirname(currentFilePath)  # Get the directory of the current file
chromaDbPath = os.path.join(baseDir, 'chromadata')

# Start ChromaDB in the background
chromaProcess = subprocess.Popen(
    ["chroma", "run", "--host", "localhost", "--port", "8000", "--path", chromaDbPath],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

try:

    chromaClient = chromadb.HttpClient(host="localhost", port=8000)
    collection = chromaClient.get_or_create_collection(name=chromaCollectionName)

    #query = " ".join(sys.argv[1:])

    print("Enter your query:")
    query = input()
    if not query:
        print("No query provided. Exiting.")
        sys.exit(1)

    queryEmbed = ollama.embed(model=ollamaModel, input=query)['embeddings']

    relatedDocs = '\n\n'.join(collection.query(query_embeddings=queryEmbed, n_results=10)['documents'][0])
    prompt = f"{query} - Answer that question using the following text as a resource: {relatedDocs}"
    noRagOutput = ollama.generate(model="mistral", prompt=query, stream=False)
    print(f"Answered without RAG: {noRagOutput['response']}")
    print("---")
    ragOutput = ollama.generate(model="mistral", prompt=prompt, stream=False)

    print(f"Answered with RAG: {ragOutput['response']}")
finally:
    # Terminate the ChromaDB process when the webserver exits
   print("Terminating ChromaDB process...")
   chromaProcess.terminate()
   chromaProcess.wait()