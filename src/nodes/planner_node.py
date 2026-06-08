# 1st Libs
import re
import json
from typing import List, Dict
from pydantic import BaseModel, Field

# 3rd Libs
from langchain_core.messages import AIMessage

# Insource
from src import agents
from src.prompts.system_prompt import get_sys_prompt
from src.rag.agent_registry import AgentRegistry

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
    
    def __init__(self, llm, agentsRegistry):
        self.llm = llm
        self.agentsRegistry = agentsRegistry
        # self.sys_prompt = f"""
        # Bạn là HarVnh, một Kiến trúc sư Hệ thống AI (Lead Architect Agent).\
        # Nhiệm vụ của bạn là nhận yêu cầu (prompt) từ người dùng, phân tích và sáng tạo một chuỗi các bước xử lý logic tuần tự (Đồ thị động).\
        # Hãy chọn các tên Node rõ ràng, mang tính hành động và sắp xếp chúng theo đúng thứ tự thực hiện.\
        # """
        
    def __call__(self, state):
        """  
        Hàm thực thi khi langgraph gọi tới
        """
        
        userPrompt = state.userMessages[-1]
        if hasattr(userPrompt, 'content'):
            userPrompt= userPrompt.content
            
        
        relevantAgents = self.agentsRegistry.query_relevant_agents(userPrompt, 3, 1.2)
        
        if not relevantAgents:
            error_msg = (
            "[ERR] Planner Node: Hệ thống không tìm thấy Agent nào phù hợp với yêu cầu của bạn.\n"
            "Vui lòng mô tả lại nhiệm vụ rõ ràng hơn hoặc bổ sung thêm Agent chuyên trách vào hệ thống."
        )
            return {
                "relevantAgents": [],
                "status": "failed",
                "resMessages": state.resMessages + [error_msg]
            }
        
        agents_context = ""
        for idx, agent in enumerate(relevantAgents):
            agents_context += f"[{idx+1}] Agent Name: {agent['name']}\nCapability: {agent['capability']}\n\n"
        
        sysPrompt = f"""Bạn là Bộ Định Tuyến Hệ Thống (Planner Router) phụ trách tạo ra đồ thị thực thi động (Dynamic Graph). Dưới đây là danh sách các Agents duy nhất bạn có quyền sử dụng để phân rã nhiệm vụ:
            {agents_context}
        Nhiệm vụ của bạn: Dựa trên yêu cầu của người dùng, hãy thiết kế một chuỗi các bước (Dynamic Graph) liên kết các Agent phù hợp lại với nhau.
        Bạn BẮT BUỘC phải trả về định dạng JSON nghiêm ngặt theo cấu trúc sau:
        {{
        "tasks": [
            {{
            "step": 1,
            "agent_name": "Tên agent được chọn từ danh sách trên",
            "task_description": "Mô tả chi tiết công việc cụ thể cho agent này"
            }}
        ]
        }}"""
        

        try:
            response = self.llm.generate_dynamic_graph(
                system_prompt=sysPrompt, 
                user_prompt=userPrompt
            )
            
            dynamicGraph = json.loads(response)
            
            return {
                "relevantAgents": relevantAgents,
                "currentPlan": dynamicGraph,
                "status": "success",
                "resMessages": state.resMessages + [f" Đã lập kế hoạch đồ thị động thành công với {len(relevantAgents)} agents!"]
            }
        except Exception as e:
            return {
                "status": "failed",
                "resMessages": state.resMessages + [f"[i] PlannerNode: Thất bại trong quá trình sinh Dynamic Graph từ LLM: {str(e)}"]
            }
        # prompt = get_sys_prompt() + f"\nYêu cầu của người dùng: {userPrompt}"
        
        # response = self.llm.with_structured_output(Plan).invoke(prompt)
        
        # return {
        #     "currentPlan": response.model_dump(),
        #     "resMessages": [AIMessage(content=response.planDescriptionMessage)]
        # }
        
