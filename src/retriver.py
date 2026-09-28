from sentence_transformers import SentenceTransformer
import chromadb



def retrieve_relevant_chunks(query:str,collection=None,embed_model=None,top_k:int=5):
    """检索与查询最相关的文本块
    参数：
        query (str): 用户查询
        top_k (int): 返回的最相关块数
    返回：
        list: 最相关的文本块列表（如果出错为None）
              列表中每个项目可以是文本内容，也可以是包含文本和元数据的字典
              如果没有结果，返回空列表
    """
    if collection is None:
        print("错误：向量数据库集合不可用。")
        return None
    if embed_model is None:
        print("错误：嵌入模型不可用。")
        return None
    try:
        # 将查询转换为嵌入向量
        query_embedding = embed_model.encode(query).tolist()
        # 查询向量数据库
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=[ 'documents','metadatas','distances' ]
        )
        # 返回结果
        # documents 字段包含检索到的分块文本
        retrieved_docs = results.get('documents', [[]])[0]
        retrieved_metadatas = results.get('metadatas', [[]])[0]
        retrieved_distances = results.get('distances', [[]])[0]
        #组合结果以便后续使用
        processed_results = []
        for i , doc in  enumerate(retrieved_docs):
            processed_results.append({
                'text': doc,
                'metadata': retrieved_metadatas[i] if i < len(retrieved_metadatas) else {},
                'distance': retrieved_distances[i] if i < len(retrieved_distances) else None
            })
        print(f"检索到 {len(processed_results)} 个分块")
        return processed_results
    except Exception as e:
        print(f"检索相关分块时出错: {e}")
        return None
#示例用法
