# 1st Libs
from pathlib import Path

# 3rd Libs
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# Insource


# =================== SOURCE ========================
class AgentRetriever:
    def __init__(self):
        self._CHROMA_DATA_DIR = Path.cwd() + "data/chroma.db"
        pass

    def initialize_agent_retriever(self) -> Chroma:
        convertModel = OpenAIEmbeddings(model= "text-embedding-3-small")
        
        if Path.exists(self._CHROMA_DATA_DIR):
            print("[i] CHORMA: Tìm thấy dữ liệu Vector cũ, đang nạp từ ổ đĩa...")
            return Chroma(
                persist_directory=self._CHROMA_DATA_DIR, 
                embedding_function=convertModel)
        
        vector_store = Chroma(
        persist_directory=self._CHROMA_DATA_DIR, 
        embedding_function=convertModel
        )
        
        texts = [agent["capability"] for agent in ALL_AGENTS]
        metadatas = [{"name": agent["name"], "capability": agent["capability"]} for agent in ALL_AGENTS]
        ids = [agent["name"] for agent in ALL_AGENTS]
        
        vector_store.add_texts(texts=texts, metadatas=metadatas, ids=ids)
        return vector_store
            