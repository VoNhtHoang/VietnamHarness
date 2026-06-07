# 1st Libs
from dotenv import load_dotenv
# 3rd Libs
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_google_genai import ChatGoogleGenerativeAI

# Insource
from src.state.state import SharedState
from src.nodes.planner_node import PlannerNode


# ============== SOURCE ===================
load_dotenv()
memory = MemorySaver()

# init
llm = ChatGoogleGenerativeAI(
    model="gemini-3.1-flash-lite",
    temperature=0.8 # càng về 1 tính sáng tạo càng cao, nhưng càng kém chính xác
)

# init node
planner_node = PlannerNode(llm)

# ================= Graph ==================
graph = StateGraph(SharedState)
graph.add_node("planner", planner_node)

# edge
graph.add_edge("planner", END)

# entrypoint
graph.set_entry_point("planner")

workflow = graph.compile(checkpointer=memory)


