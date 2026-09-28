# requests和BeautifulSoup使用示例
# 安装命令：pip install requests beautifulsoup4
# 以pypdf为例（安装命令：pip install pypdf）
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

def load_text_file(file_path):
    """从文本文件中读取内容。"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return (content,file_path)
    except FileNotFoundError:
        print(f"错误：文件未在 {file_path} 找到")
        return None
    except Exception as e:
        print(f"读取文件 {file_path} 时出错：{e}")
        return None

def load_pdf_text(file_path):
    """从PDF文件中提取文本内容。"""
    try:
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text: # 检查文本提取是否成功
                text += page_text + "\n" # 在页之间添加换行符
        return (text.strip(),file_path) # 移除开头/结尾的空白字符
    except FileNotFoundError:
        print(f"错误：文件未在 {file_path} 找到")
        return None
    except Exception as e:
        print(f"读取PDF文件 {file_path} 时出错：{e}")
        return None


def load_web_page_text(url):
    """从网页URL获取并提取文本内容。"""
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}) # 做一个有礼貌的爬虫
        response.raise_for_status() # 对于错误的HTTP状态码（4xx或5xx）抛出异常

        soup = BeautifulSoup(response.content, 'html.parser')#html.parser是Python内置的HTML解析器，速度快且不依赖外部库

        # 基本文本提取（可以进行大量优化）
        # 移除脚本和样式元素(JS css)
        for script_or_style in soup(["script", "style"]):#等价于soup.find_all(["script", "style"])
            script_or_style.decompose()

        # 获取文本，使用分隔符确保元素之间有空格
        text = soup.get_text(separator=' ', strip=True)
        return (text,url)

    except requests.exceptions.RequestException as e:
        print(f"获取URL {url} 时出错：{e}")
        return None
    except Exception as e:
        print(f"从 {url} 解析HTML时出错：{e}")
        return None

"""# 使用示例：
web_url = 'https://cn.bing.com/search?q=python%E5%A4%9A%E8%A1%8C%E6%B3%A8%E9%87%8A&form=ANNTH1&refig=b3bf4b41c89943eee61fa8f6f6bc01c8&pc=ASTS'
web_text_content = load_web_page_text(web_url)

if web_text_content:
    print(f"成功从 {web_url} 加载文本")
    # 继续处理web_text_content...
else:
    print(f"无法从 {web_url} 加载文本")
"""
# 使用示例：
'''
file_path = 'documents/my_document.txt'
text_content = load_text_file(file_path)

if text_content:
    print(f"成功从 {file_path} 加载内容")
    # 继续处理text_content...
'''

