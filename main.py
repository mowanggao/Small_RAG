from src.rag_pipeline import RAG_Pipeline

if __name__ == '__main__':
    rag = RAG_Pipeline()
    while True:
        choice = input("请输入选项（1.添加 2.查询 3.退出）:    ")
        if choice == "1":
            file_path = input("请输入文件路径:    ")
            rag.add_to_db(file_path)
        elif choice == "2":
            query = input("请输入查询内容:    ")
            answer = rag.chat(query)
            print(answer)
        elif choice == "3":
            break
        else:   
            print("无效选项，请重新输入")