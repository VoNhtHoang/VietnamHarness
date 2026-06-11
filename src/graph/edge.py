# 1st Libs
import sys
from typing import Optional, List, Dict
from pydantic import BaseModel, Field

# 3rd Libs
from langgraph.graph import StateGraph, END


# Insource
from src.graph.node import Node
# ===================== SOURCE =========================

class GraphEdge(BaseModel):
    source: str = Field(description="Tên node bắt đầu")
    target: str = Field(description="Tên node mục tiêu, bắt buộc có giá trị nếu không phải là conditional edge.")
    isCondition: bool = Field(default=False, description="Cạnh này có phải là cạnh điều kiện không")
    
    routerCode: Optional[str] = Field(
        default=None, 
        description="Đoạn code Python logic rẽ nhánh. Code này PHẢI đọc từ biến 'state' và gán kết quả vào biến 'next_node'. Ví dụ: 'if state[\"errors\"]: next_node = \"fix_node\"\\nelse: next_node = \"deploy_node\"'"
    )
    
    conditionalMapping: Optional[Dict[str, str]] = Field(
        default=None, 
        description="Ánh xạ chuỗi trả về từ router_code sang tên Node thực tế trong LangGraph. Ví dụ: {'fix_node': 'coding_agent', 'deploy_node': 'devops_agent'}, tất nhiên là các node được ánh xạ tới bắt buộc phải có trong danh sách agent được cung cấp"
    )
    
# class GraphEdge(BaseModel):
    
#     entryPoint: str = Field(description="Tên (name) node bắt đầu")
    
#     endPoint: str = Field(description="Tên node kết thúc cố định nếu không có điều kiện")
    
#     conditionFuncName: Optional[str]  = Field(
#         None, 
#         description="Tên hàm điều kiện nếu đây là conditional edge."
#         )
    
#     conditionMapping: Optional[Dict[str, str]] = Field(
#         None, 
#         description="Dictionary về kết quả hàm điều kiện sang node tiếp theo, ví dụ: {'success':'test_node', 'fail':'end'}"
#         )

class DynamicGraph(BaseModel):
    nodes: List[Node] = Field(description="Danh sách các node, kèm mô tả nhiệm vụ chi tiết của mỗi node cần cho graph")
    edges: List[GraphEdge] = Field(description="Danh sách toàn bộ các cạnh nối tĩnh và cạnh điều kiện")
    entryPoint: str = Field(description="Tên node xuất phát (entrypoint)")
    graphDescription: str = Field(description="Mô tả ngắn gọn về Dynamic Graph được generate,  tổng quan về cách các agent được dùng.")
    
    
def createDynamicRouter(routerCode: str):
    """_summary_
    Biến chuỗi code từ LLM thành 1 hàm router graph hoàn chỉnh
    Args:
        routerCode (str): chuỗi trả về từ GraphEdge
    """
    
    def router(state):
        localVars = {"state": state, "nextNode": None}
        globalVars =   {"__builtins__": {}} # giới hạn -> tránh inject code / prompt
        
        try:
            exec(routerCode, localVars, globalVars)
            
            result = localVars.get("nextNode")
            if not result:
                raise ValueError("[ERR] Planner Node - Edge: Code conditional edege của LLM không gán giá trị cho NextNode")
            
            return result

        except Exception as e:
            print(f"[Router Error] Planner Node - Edge: Lỗi thực thi code từ LLM: {e}", file=sys.stderr)
            # Fallback an toàn: Nếu lỗi, đẩy về END hoặc một node sửa lỗi
            return "end"
    
    return router


