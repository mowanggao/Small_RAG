from src.load_file import load_text_file
from src.create_db import get_collection
from src.chunking import split_text
from src.retriver import retrieve_relevant_chunks
from src.embeding import get_embedding,Eembedding
from src.llm_client import *
class RAG_Pipeline:
    def __init__(self):
        self.collection = get_collection()
        self.embed_model = Eembedding()
        self.llm = init_llm_client()
    def chat(self,query:str):
        relevant_chunks = retrieve_relevant_chunks(query,self.collection,self.embed_model,top_k=3)
        if relevant_chunks:
            augmented_prompt = create_augmented_prompt(query,[content['text'] for content in relevant_chunks])
            return chat(self.llm,augmented_prompt)
        else:
            print("No relevant chunks found.")
    def add_to_db(self,file_path):
        data_chunk = split_text(load_text_file(file_path))
        get_embedding(data_chunk)
    def test_chat(self,query:str):
        return chat(self.llm, query)
        