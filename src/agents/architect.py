""" 

Solve Coding Problems - Usually work with whole architect prompting

"""

# 1st Libs
from typing import List
from pydantic import BaseModel, Field, ConfigDict

# 3rd Libs


# Insource
from src.agents.init_base import File, SubTask, SubTaskList


# ================== SOURCE ========================
    
class ArchitectMetadata(BaseModel):
    name: str = Field(default="architect_coding_agent", description="Tên định danh bắt buộc")
    capability : str = Field(
        default="Chuyên xử lý các yêu cầu của người dùng liên quan đến tạo một dự án coding, phân tích và tạo ra các tasks nhỏ hơn (sub-tasks) một cách chi tiết với mục đích hoàn thành yêu cầu ban đầu của người dùng. Mỗi sub-task sẽ gắn liền mới một file cần tạo hoặc sửa, và mô tả chi tiết về các bước để hoàn thành, ví dụ: 'import các thư viện cần thiết', 'code các hàm, lớp, biến cần thiết', 'code chi tiết các thành phần', vâng vâng. Lưu ý: Nếu yêu cầu có thể được xử lí bởi 1 sub-task thì đừng tạo ra 3 sub-tasks."
        )
    
class ArchitectNode:
    """
    A Node that help user solve their requests by the ways of spling that request into subtasks
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.metadata = ArchitectMetadata()
        self.architectPrompt = """
        
        """
        

    def __call__(self, state):
        pass

