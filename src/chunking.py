import uuid
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_text(object_tuple):
    try:
        """分割文本"""
        #初始化分割器
        recursive_splitter = RecursiveCharacterTextSplitter(
            separators = ["\n\n", "\n", " ", ""],#分隔符列表
            chunk_size = 250,#字符计数
            chunk_overlap  = 50,#重叠字符数
            length_function = len,
            is_separator_regex = False,
        )
        #分割文本
        fixed_chunks = recursive_splitter.split_text(object_tuple[0])
        #查看
        if fixed_chunks:#建立数据块
            data_chunk = []
            print(f"创建的块数：{len(fixed_chunks)}\n")
            for i,chunk in enumerate(fixed_chunks):
                context = {}
                context["text_context"] = chunk
                context["metadata"] = object_tuple[1]
                context["id"] = uuid.uuid4()
                data_chunk.append(context)
            return data_chunk
        else:
            return []  # 优化：返回空列表而不是None，避免后续None报错   
    except Exception as e:
        print(f"分割文本时发生错误：{e}")

        
