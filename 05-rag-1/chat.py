from langchain_openai import OpenAIEmbeddings   #Vector Embedding
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore #Store connection

load_dotenv() # Vectore Embeding

# Query
query = input("> ")

# Vectore Embeding
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")
embeding = embeddings.embed_query(query)

# Store connection
vector_store = QdrantVectorStore.from_existing_collection(
    #documents=query,
    url="http://localhost:6333/", #database url
    collection_name = "learning_vector", #database collection name
    embedding=embeddings
)

# Search vactore similarity of Query
result = vector_store.similarity_search_by_vector(embeding)
print(result[0])