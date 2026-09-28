import os
from openai import OpenAI
from dotenv import load_dotenv

def create_augmented_prompt(query:str,context_chunk:list[str])->str:
    context = "\n\n".join(context_chunk)
    prompt = f"""请根据以下上下文回答查询。如果上下文不包含答案，请说明。
    上下文：
    {context}
    查询：{query}
    答案："""
    return prompt

def init_llm_client():
    load_dotenv()  # 加载环境变量
    try:
        client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url="https://ws-ithji003x145e7vv.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
        )
        return client
    except Exception as e:
        print(f"错误信息: {e}")
        print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")
def chat(client, prompt: str):#参数：用户客户端对象，查询，上下文块
    try:
        response = client.chat.completions.create(
            model="qwen3.7-plus",
            messages=[
                {"role":'system',"content":"You are a helpful assistant."},
                {"role": "user", "content": f"{prompt}"}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"错误信息: {e}")
        print("请参考文档：https://help.aliyun.com/model-studio/developer-reference/error-code")


        
