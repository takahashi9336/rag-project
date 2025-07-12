import os 
# from langchain_community.embeddings import OllamaEmbeddings 
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings

CHROMA_PATH = os.getenv('CHROMA_PATH', './chroma_store') 
COLLECTION_NAME = os.getenv('COLLECTION_NAME', 'rag-collection') 
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'snowflake-arctic-embed2:568m') 
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

def get_vector_db(): 
    embedding = OllamaEmbeddings(model=EMBEDDING_MODEL)

    db = Chroma(
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_PATH,
        embedding_function=embedding
    )
    return db