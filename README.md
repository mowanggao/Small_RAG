# RAG 本地知识库问答系统

一个基于 **检索增强生成（Retrieval-Augmented Generation, RAG）** 的轻量级本地知识库问答 demo。
把本地文本（`.txt`，同样支持 PDF / 网页）切块、向量化后存入 [Chroma](https://www.trychroma.com/) 向量数据库；
提问时先检索最相关的文本片段，再拼装成提示词交给大模型（阿里云百炼 `qwen3.7-plus`）生成回答。

整个过程带命令行交互菜单，适合作为学习 RAG 完整链路的入门项目。

---

## 一、功能特性

- **文档入库**：读取本地文本 → 递归分块 → 向量化 → 持久化到 Chroma。
- **语义检索**：用 `all-MiniLM-L6-v2` 把问题和文档块映射到同一向量空间，按余弦相似度取 Top-K。
- **增强问答**：把检索到的上下文与问题拼成 prompt，交给大模型生成最终答案。
- **持久化存储**：向量库落在 `data/vector_db/`，重启程序不会丢失已有知识。
- **可扩展加载器**：除纯文本外，`src/load_file.py` 已实现 PDF（`pypdf`）与网页（`requests` + `BeautifulSoup`）解析函数，可按需接入。

---

## 二、目录结构

```
RAG/
├── main.py                 # 程序入口：命令行交互菜单（添加 / 查询 / 退出）
├── requirement.txt         # 项目依赖清单
├── .env                    # 存放 OPENAI_API_KEY（大模型密钥），已被 .gitignore 忽略
├── .gitignore
├── astrocortex.txt         # 示例知识文本
├── 123.txt                 # 示例知识文本
├── data/
│   ├── my_document.txt     # 示例知识文本
│   └── vector_db/          # Chroma 向量库持久化目录（自动生成）
└── src/
    ├── __init__.py
    ├── rag_pipeline.py     # 核心编排：串联「入库」与「问答」两条流程
    ├── load_file.py        # 文件加载：txt / pdf / 网页
    ├── chunking.py         # 文本分块（RecursiveCharacterTextSplitter）
    ├── embeding.py         # 向量化并把分块写入 Chroma 集合
    ├── create_db.py        # 创建 / 获取 Chroma 持久化集合
    ├── retriver.py         # 向量检索：查询 → 相似片段
    ├── llm_client.py       # 大模型客户端初始化与对话、prompt 拼装
    └── test.py             # 预留的加载器示例（LangChain 写法，未启用）
```

---

## 三、工作原理

### 1. 入库流程（`1.添加`）

```
文本文件
  └─ load_file.load_text_file()      # 读出 (正文, 文件路径)
       └─ chunking.split_text()      # RecursiveCharacterTextSplitter 分块
            │                        #   chunk_size=250, chunk_overlap=50
            │                        #   每块 = {text_context, metadata(来源路径), id(uuid)}
            └─ embeding.get_embedding()
                 └─ create_db.get_collection()   # 获取 Chroma 集合 my_documents
                      └─ SentenceTransformer('all-MiniLM-L6-v2') 向量化并写入
```

### 2. 问答流程（`2.查询`）

```
用户问题
  └─ retriver.retrieve_relevant_chunks()   # 问题向量化 → Chroma 余弦检索 Top-K(=3)
       └─ llm_client.create_augmented_prompt()   # 把检索片段拼进 prompt
            └─ llm_client.chat()                 # 调用 qwen3.7-plus 生成回答
```

如果检索不到任何相关片段，程序会打印 `No relevant chunks found.` 并返回空结果。

---

## 四、环境要求

- **Python**：3.10（本项目在 3.10.20 下开发验证）
- **操作系统**：Windows / Linux / macOS 均可
- **网络**：首次运行需联网下载嵌入模型 `all-MiniLM-L6-v2`；问答需能访问阿里云百炼接口

### 安装依赖

```bash
# 建议使用虚拟环境
conda create -n rag python=3.10 -y
conda activate rag

# 安装依赖
pip install -r requirement.txt
```

> 说明：`sentence-transformers` 会依赖 `torch`、`transformers`；Chroma 的默认嵌入函数会依赖 `onnxruntime`。
> 如果安装 `torch` 需要特定 CUDA 版本，请参考 [PyTorch 官网](https://pytorch.org/get-started/locally/) 选择对应命令。

---

## 五、配置密钥

在项目根目录创建 `.env` 文件（仓库中已有一份模板），填入你的 API Key：

```dotenv
OPENAI_API_KEY="你的阿里云百炼 API Key"
```

代码在 `src/llm_client.py` 中使用阿里云百炼的 **OpenAI 兼容接口**：

```python
OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://ws-ithji003x145e7vv.cn-beijing.maas.aliyuncs.com/compatible-mode/v1",
)
```

如需改用其他模型或服务，修改 `init_llm_client()` 的 `base_url` 与 `chat()` 中的 `model` 字段即可。

> 安全提醒：`.env` 已被 `.gitignore` 忽略，请勿把真实密钥提交到仓库。

---

## 六、使用流程

在 `RAG/` 目录下运行：

```bash
python main.py
```

启动后进入交互菜单：

```
请输入选项（1.添加 2.查询 3.退出）:
```

| 选项 | 说明 | 操作示例 |
| --- | --- | --- |
| `1` | 添加文件到知识库 | 输入 `data/my_document.txt`，程序会分块并写入向量库 |
| `2` | 查询知识库 | 输入问题（如「地球是第几颗行星？」），返回大模型生成的答案 |
| `3` | 退出程序 | — |

**完整示例：**

```text
请输入选项（1.添加 2.查询 3.退出）:    1
请输入文件路径:    data/my_document.txt
创建的块数：3
已插入3条文档

请输入选项（1.添加 2.查询 3.退出）:    2
请输入查询内容:    火星为什么是红色的？
火星被称为“红色星球”，是因为其表面富含氧化铁（铁锈），呈现红色外观。
```

> 提示：可以多次执行「1.添加」把多个文件加入同一个向量库；重复添加同一文件会产生重复内容。

---

## 七、模块速览

| 模块 | 关键函数 | 职责 |
| --- | --- | --- |
| `main.py` | — | 命令行菜单，调度添加 / 查询 |
| `src/rag_pipeline.py` | `RAG_Pipeline.chat` / `add_to_db` | 编排入库与问答主流程 |
| `src/load_file.py` | `load_text_file` / `load_pdf_text` / `load_web_page_text` | 加载 txt、PDF、网页文本 |
| `src/chunking.py` | `split_text` | 递归分块并附加元数据与唯一 id |
| `src/embeding.py` | `Eembedding` / `get_embedding` | 构建嵌入模型、写入 Chroma |
| `src/create_db.py` | `get_collection` | 获取持久化集合（余弦距离） |
| `src/retriver.py` | `retrieve_relevant_chunks` | 向量检索 Top-K |
| `src/llm_client.py` | `init_llm_client` / `chat` / `create_augmented_prompt` | 大模型调用与 prompt 拼装 |

---

## 八、常见问题

- **首次查询很慢**：第一次会下载 `all-MiniLM-L6-v2` 模型（约几十 MB），之后就缓存在本地。
- **报错「无效选项」**：菜单只接受 `1` / `2` / `3`，注意不要输入多余空格或中文标点。
- **返回 `No relevant chunks found.`**：知识库为空或问题与现有文档差异过大，先执行「1.添加」。
- **大模型调用报错**：检查 `.env` 中的 `OPENAI_API_KEY` 是否有效、网络能否访问 `base_url`，报错码可参考[阿里云百炼错误码文档](https://help.aliyun.com/model-studio/developer-reference/error-code)。
- **中文检索效果一般**：默认嵌入模型 `all-MiniLM-L6-v2` 以英文为主，若知识库以中文为主，建议替换为中文更强的模型（如 `bge-small-zh` 等），并同步修改 `create_db.py` 与 `embeding.py` 中的模型名。

---

## 九、可扩展方向

- 在 `main.py` 中接入 `load_pdf_text` / `load_web_page_text`，支持 PDF 与网页入库。
- 增加「删除 / 重建向量库」等管理功能（Chroma 提供 `delete` 与 `reset`）。
- 加入流式输出与多轮对话历史，提升问答体验。
