from pathlib import Path  
from langchain_community.document_loaders import PyPDFLoader #loading
from langchain_text_splitters import RecursiveCharacterTextSplitter #Chunking
from langchain_openai import OpenAIEmbeddings   #Vector Embedding
from dotenv import load_dotenv
from langchain_qdrant import QdrantVectorStore #Store

load_dotenv()

#Loading
pdf_path = Path(__file__).parent / "nodejs.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs = loader.load() # Read pdf file

# print(docs[124])

#Chunking
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

# print(len(all_splits))
# print(all_splits[5].page_content)

#Vector embedings
embeddings = OpenAIEmbeddings(model="text-embedding-3-large")

# Store
# Using [embedding_model] create embeddings of [split_docs] and store in DB
vector_store = QdrantVectorStore.from_documents(
    documents=all_splits,
    url="http://localhost:6333/", #database url
    collection_name = "learning_vector", #database collection name
    embedding=embeddings
)

print("indexing of documents is done")