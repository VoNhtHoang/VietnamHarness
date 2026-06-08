# 1st Libs
from ssl import MemoryBIO

from dotenv import load_dotenv
# 3rd Libs
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

# Insource
from src import agents
from src.utils.memory import SqliteMemoryManager
from src.state.state import SharedState
from src.rag.agent_registry import AgentRegistry
from src.nodes.planner_node import PlannerNode


# ============== SOURCE ===================
load_dotenv()

def _main_router(state: SharedState):
    if state.status == "failed":
        return "end_flow"
    return "continue_flow"


def _init_workflow():
    
    sqlMemManager = SqliteMemoryManager()
    memory = sqlMemManager._connect()
    
    # agentsReg & sync vectordb
    agentsRegistry = AgentRegistry()
    agentsRegistry.scan_sync_agents()
    
    # init
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-flash-lite",
        temperature=0.8 # càng về 1 tính sáng tạo càng cao, nhưng càng kém chính xác
    )

    # init node
    planner_node = PlannerNode(llm, agentsRegistry)

    # ================= Graph ==================
    graph = StateGraph(SharedState)
    graph.add_node("planner", planner_node)

    # edge
    graph.add_edge("planner", END)
    graph.add_conditional_edges(
        "planner",
        _main_router,
        {
            "end_flow": END,
            "continue_flow": END
        }
    )
    # entrypoint
    graph.set_entry_point("planner")

    workflow = graph.compile(checkpointer=memory)
    
    return workflow


# from contextlib import asynccontextmanager
# from fastapi import FastAPI
# import sqlite3

# conn = None

# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     global conn
#     # 1. Khi FastAPI khởi động: Mở kết nối
#     conn = sqlite3.connect("harness_sessions.db", check_same_thread=False)
#     yield
#     # 2. Khi FastAPI tắt (Shutdown): Chủ động đóng kết nối
#     if conn:
#         conn.close()
#         print("Đã chủ động đóng kết nối SQLite an toàn.")

# app = FastAPI(lifespan=lifespan)