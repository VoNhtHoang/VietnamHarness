# 1st Libs
import sys
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

# 3rd Libs

# Insource

# ===================== SOURCE =========================

class Node(BaseModel):
    name: str = Field(
        description="Tên định danh của node (ví dụ: 'crawl_data', 'analyze_content', 'send_email'). Viết thường, không dấu, phân tách bằng dấu gạch dưới.")
    
    description: str = Field(
        description="Mô tả cụ thể các công việc sẽ làm trong Node này, có thể chia nhỏ thành các task nhỏ để làm tuần tự."
        )
    
    
# class Plan(BaseModel):
#     nodes: List[Node] = Field(description="Chứa các nodes cần để thực hiện yêu cầu của người dùng")
#     planDescriptionMessage: str = Field("Câu trả lời ngắn gọn, xúc tích (không phải lý do) dành cho người dùng, mô tả về kiến trúc graph gồm các node sẽ được thực thi để hoàn thành yêu cầu của người dùng.")
#     # Messages này sẽ được hiển thị cho người dùng, yêu cầu người dùng xác nhận: chấp thuận / từ chối. Nếu người dùng chấp thuận, tiến hành thực thi graph. Ngược lại, hãy tạo một plan mới.")
