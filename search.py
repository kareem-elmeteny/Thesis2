import sys, chromadb, ollama

chromaCollectionName = "amazonReviews"
ollamaModel = "nomic-embed-text"

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