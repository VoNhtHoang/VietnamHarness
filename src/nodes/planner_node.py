# 1st Libs
import re
import json
from typing import List, Dict, Optional
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

# 3rd Libs
from langchain_core.messages import AIMessage

# Insource
from src import agents
from src.prompts.system_prompt import get_sys_prompt
from src.rag.agent_registry import AgentRegistry
from src.graph.edge import createDynamicRouter, DynamicGraph
from src.state.state import SharedState
    
# =================== SOURCE ============================
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
            
        
        relevantAgents = self.agentsRegistry.query_relevant_agents(userPrompt, 3, 1.5)
        
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
        
        prompt = f"""Bạn là Bộ Định Tuyến Hệ Thống (Planner Router) phụ trách tạo ra đồ thị thực thi động (Dynamic Graph). Dưới đây là danh sách các Agents duy nhất bạn có quyền sử dụng để phân rã nhiệm vụ:
            {agents_context}
        Nhiệm vụ của bạn: Dựa trên yêu cầu của người dùng, hãy thiết kế một chuỗi các bước (Dynamic Graph) liên kết các Agent phù hợp lại với nhau, có thể có cả conditional edges, ...
        
        Yêu cầu của người dùng:
        {userPrompt}
        """
        
        # Bạn BẮT BUỘC phải trả về định dạng JSON nghiêm ngặt theo cấu trúc sau:
        # {{
        # "tasks": [
        #     {{
        #     "step": 1,
        #     "agent_name": "Tên agent được chọn từ danh sách trên",
        #     "task_description": "Mô tả chi tiết công việc cụ thể cho agent này"
        #     }}
        # ]
        # }}
        
        try:
            response = self.llm.with_structured_output(DynamicGraph).invoke(prompt)
            
            dynamicGraph = self.compileDynamicGraph(
                plan = response
            )
            
            # dynamicGraph = json.loads(response)
            return {
                "relevantAgents": relevantAgents,
                "currentPlan": response.nodes,
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
        
    def compileDynamicGraph(self, plan: DynamicGraph):
        workflow = StateGraph(SharedState)
        for node in plan.nodes:
            nodeName = node.name
            agentClass = self.agentsRegistry.getAgentClass(nodeName)
            agentInstance = agentClass(self.llm)
            workflow.add_node(nodeName, agentInstance)
            
        # entrypoint
        workflow.set_entry_point(plan.entryPoint)
        
        # conditional Edges
        for edge in plan.edges:
            if not edge.isCondition:
                workflow.add_edge(edge.source, edge.target)
            
            else:
                routerFunc = createDynamicRouter(edge.routerCode)
                
                print(edge.conditionalMapping)
                print(routerFunc)

                workflow.add_conditional_edges(
                    edge.source,
                    routerFunc,
                    edge.conditionalMapping
                )
        
        return workflow.compile()
            
            
        
