# 1st Libs
from typing import List, Dict
from pydantic import BaseModel, Field

# 3rd Libs
from langchain_core.messages import AIMessage

# Insource
from src.prompts.system_prompt import get_sys_prompt

class Node(BaseModel):
    name: str = Field(
        description="Tên định danh của node (ví dụ: 'crawl_data', 'analyze_content', 'send_email'). Viết thường, không dấu, phân tách bằng dấu gạch dưới.")
    
    description: str = Field(
        description="Mô tả cụ thể các công việc sẽ làm trong Node này, có thể chia nhỏ thành các task nhỏ để làm tuần tự."
        )
    
class Plan(BaseModel):
    nodes: List[Node] = Field(description="Chứa các nodes cần để thực hiện yêu cầu của người dùng")
    planDescriptionMessage: str = Field("Câu trả lời ngắn gọn, xúc tích (không phải lý do) dành cho người dùng, mô tả về kiến trúc graph gồm các node sẽ được thực thi để hoàn thành yêu cầu của người dùng. Messages này sẽ được hiển thị cho người dùng, yêu cầu người dùng xác nhận: chấp thuận / từ chối.")
    #Nếu người dùng chấp thuận, tiến hành thực thi graph. Ngược lại, hãy tạo một plan mới.")
    

class PlannerNode:
    """
    Initialize a Planner Agent that helps create a Plan with Nodes.
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.sys_prompt = f"""
        Bạn là HarVnh, một Kiến trúc sư Hệ thống AI (Lead Architect Agent).\
        Nhiệm vụ của bạn là nhận yêu cầu (prompt) từ người dùng, phân tích và sáng tạo một chuỗi các bước xử lý logic tuần tự (Đồ thị động).\
        Hãy chọn các tên Node rõ ràng, mang tính hành động và sắp xếp chúng theo đúng thứ tự thực hiện.\
        """
    def __call__(self, state):
        """  
        Hàm thực thi khi langgraph gọi tới
        """
        
        userPrompt = state.get("")
        prompt = get_sys_prompt() + f"\nYêu cầu của người dùng: {userPrompt}"
        
        response = self.llm.with_structured_output(Plan).invoke(prompt)
        
        return {
            "currentPlan": response.model_dump(),
            "resMessages": [AIMessage(content=response.planDescriptionMessage)]
        }
        
