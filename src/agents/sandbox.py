# 1st Libs
from typing import List, Optional, Dict, Any
from unittest.mock import Base
from pydantic import BaseModel, Field

# 3rd Libs
from langchain.agents import create_agent

# Insource


# ==================== SOURCE ====================
class SandboxMetaData(BaseModel):
    """ Định danh Node Sandbox """
    
    name: str = Field(default="sandbox_agent", description="Tên định danh bắt buộc của node (agent)")
    capability: str = Field(
        default="""
        Chuyên nhận các plan, nhiệm vụ liên quan về run command, isolate, sandboxing từ các agent khác và thực thi chúng trong một môi trường được tạo riêng, đảm bảo an toàn cho hệ thống của người dùng.
        """,
        description="Năng lực chi tiết được lưu vào VectorDB để PlannerNode tìm kiếm."
    )
    
class SandboxAction(BaseModel):
    pass

class SandboxAgent:
    """ """
    pass
