from sentence_transformers import SentenceTransformer
from .create_db import get_collection

def Eembedding():
    model = SentenceTransformer('all-MiniLM-L6-v2')
    return model

def get_embedding(data_chunk):
    try:
        collection = get_collection()
        # 'embeddings' 现在包含一个列表，其中是已准备好用于向量数据库的对象
        #collection.add每个参数接受一个列表
        documents = [chunk['text_context'] for chunk in data_chunk]
        ids = [str(chunk['id']) for chunk in data_chunk]
        metadata = [{'source':chunk['metadata']} for chunk in data_chunk]
        collection.add(
            documents=documents,
            ids=ids,
            metadatas=metadata,
            )
        print(f"已插入{len(data_chunk)}条文档")
    except Exception as e:
        print(f"Error: {e}")
        print("添加数据库失败")

