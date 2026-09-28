# 示例（语法可能因框架而异）
from rag_framework.document_loaders import PyPDFLoader, WebBaseLoader

# pdf_loader = PyPDFLoader("documents/research_paper.pdf")
# web_loader = WebBaseLoader("https://example-documentation-site.com/page")

# pdf_documents = pdf_loader.load() # 返回Document对象列表
# web_documents = web_loader.load() # 返回Document对象列表

# print(pdf_documents[0].page_content)
# print(pdf_documents[0].metadata) # {'source': 'documents/research_paper.pdf', 'page': 0}
