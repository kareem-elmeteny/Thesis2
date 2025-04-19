import json
import re

import ollama

def extractTextFromJson(filePath :str): 
    with open(filePath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    product_name = data.get("productName", "Unknown Product")
    reviews = data.get("reviews", [])

    result = []
    for review in reviews:
        #name = review.get("name", "Anonymous")
        location = review.get("location", "Unknown Location")
        rating = review.get("rating", "No Rating")
        result.append(f'A customer reviewed product "{product_name}" in "{location}" and gave it a rating of "{rating}"')
        review_text = review.get("review-body", "")
        if review_text:
            result.append(f'Review: "{review_text}"')
        
    return "\n".join(result)

def getProductName(filePath :str):
    with open(filePath, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    product_name = data.get("productName", "Unknown Product")
    return product_name

def readJsonFiles(directoryPath :str):
    import os
    jsonFiles = []
    textContents = {}
    for filename in os.listdir(directoryPath):
        if filename.endswith('.json'):
            filePath = os.path.join(directoryPath, filename)
            productName = getProductName(filePath)
            textContent = extractTextFromJson(filePath)
            textContents[productName] = textContent
            
    return textContents

def chunkSplitter(text, chunk_size=100):
  words = re.findall(r'\S+', text)

  chunks = []
  currentChunk = []
  wordCount = 0

  for word in words:
    currentChunk.append(word)
    wordCount += 1

    if wordCount >= chunk_size:
      chunks.append(' '.join(currentChunk))
      currentChunk = []
      wordCount = 0

  if currentChunk:
    chunks.append(' '.join(currentChunk))

  return chunks

def getEmbedding(chunks, modelName="nomic-embed-text"):
  embeds = ollama.embed(model=modelName, input=chunks)
  return embeds.get('embeddings', [])

