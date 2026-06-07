# 1st Libs
import os

from typing import Annotated, Sequence, Dict, Any, Optional,List
from pydantic import BaseModel, ConfigDict, Field

# 3rd Libs
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage

# Insource
from src.nodes.planner_node import Plan

class SharedState(BaseModel):
    """ Shared State for all agents, sub-tasks """
    
    llmModel: str = Field(
        default="gemini-3.1-flash-lite", 
        description="current used llmModel"
        )
    
    userMessages: Annotated[Sequence[BaseMessage], add_messages] =  Field(description="Save user's history chat in current session")
    
    currentPlan: Optional[Dict[str, Any]] = Field("Chứa danh sách các nodes mà LLM đề xuất")
    # currentPlanGraph: StateG
     
    resMessages: Annotated[Sequence[BaseMessage], add_messages] = Field(description="Messages nhận từ LLM")
    status: str = "DONE"
    # mcp_servers: McpServer
    # mcpConnected: int = 0
    
    model_config = ConfigDict(extra="allow")
    
    