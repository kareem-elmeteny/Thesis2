import os
import subprocess
import chromadb
from extract_text import readJsonFiles, chunkSplitter, getEmbedding

chromaCollectionName = "amazonReviews"
ollamaModel = "nomic-embed-text"

# Get the absolute path of the current Python file
currentFilePath = os.path.abspath(__file__)
baseDir = os.path.dirname(currentFilePath)  # Get the directory of the current file
chromaDbPath = os.path.join(baseDir, 'chromadata')
dataPath = os.path.join(baseDir, 'data')

# Start ChromaDB in the background
chromaProcess = subprocess.Popen(
    ["chroma", "run", "--host", "localhost", "--port", "8000", "--path", chromaDbPath],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

try:
   chromaClient = chromadb.HttpClient(host="localhost", port=8000)
   jsonDocsPath = dataPath
   textData = readJsonFiles(jsonDocsPath)

   if any(collection.name == chromaCollectionName for collection in chromaClient.list_collections()):
      chromaClient.delete_collection(chromaCollectionName)
   collection = chromaClient.get_or_create_collection(name=chromaCollectionName, metadata={"hnsw:space": "cosine"}  )


   for productName, text in textData.items():
      chunks = chunkSplitter(text)
      embeds = getEmbedding(chunks, ollamaModel)
      chunknumber = list(range(len(chunks)))
      ids = [productName + str(index) for index in chunknumber]
      metadatas = [{"source": productName} for index in chunknumber]
      collection.add(ids=ids, documents=chunks, embeddings=embeds, metadatas=metadatas)
finally:
   # Terminate the ChromaDB process when the webserver exits
   print("Terminating ChromaDB process...")
   chromaProcess.terminate()
   chromaProcess.wait()