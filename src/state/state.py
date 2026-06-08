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
    
    relevantAgents: List[Dict[str, Any]] = Field(default=[], description="Danh sách Agent phù hợp quét từ VectorDB")
    
    currentPlan: Optional[Dict[str, Any]] = Field(default=None, description="Chứa danh sách các nodes mà LLM đề xuất")
     
    resMessages: Annotated[Sequence[BaseMessage], add_messages] = Field(default=[], description="Messages nhận từ LLM")
    
    status: str = Field(default="processing", description="Trạng thái hệ thống: processing, failed, approved")
    
    model_config = ConfigDict(extra="allow")
    
    