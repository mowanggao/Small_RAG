import chromadb
from pathlib import Path
from chromadb.utils.embedding_functions import  SentenceTransformerEmbeddingFunction

Base_path = Path(__file__).parent.parent    
Data_db = Base_path / "data"/"vector_db"

def get_collection():#返回集合
    client =  chromadb.PersistentClient(path=str(Data_db))  
    model = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    collection = client.get_or_create_collection(
    name="my_documents",
    embedding_function=model,
    metadata={"hnsw:space":"cosine"}
    )
    return collection

