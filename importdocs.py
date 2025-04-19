import chromadb
from extract_text import readJsonFiles, chunkSplitter, getEmbedding

chromaCollectionName = "amazonReviews"
ollamaModel = "nomic-embed-text"

chromaClient = chromadb.HttpClient(host="localhost", port=8000)
jsonDocsPath = "./data"
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