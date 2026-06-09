# 1st Libs
from csv import Error
import importlib
import inspect
from pathlib import Path

# 3rd Libs
import chromadb
from chromadb.utils import embedding_functions

# Insource


# ======================= SOURCE =============================
class AgentRegistry:
    def __init__(self, dbPath="./agent_vector_db"):
        # self.agentsDir = Path("src/agents")
        self.client = chromadb.PersistentClient(path = dbPath)
        
        
        # Đoạn này khá phân vân nên dùng emb func hay call api llm
        self.embFunction = embedding_functions.DefaultEmbeddingFunction()
        self.collection = self.client.get_or_create_collection(
            name="vietnamHarness_collection",
            embedding_function= self.embFunction
        )
        

    def scan_sync_agents(self, agentsDir: str ="src/agents"):
        """ Quét các agents hiện có trong src/agents và cập nhật metadata """
        
        if not Path.exists(Path(agentsDir)):
            print("[W] Không tìm thấy đường dẫn đến các agents")
            
            return
        
        agentsCount: int  =0
        for filePath in Path(agentsDir).glob("*.py"):
            if filePath.name == "__init__.py" or filePath.name.__contains__("init_base"):
                continue
            
            moduleName = f"{agentsDir.replace("/",".")}.{filePath.stem}"
            try:
                module = importlib.import_module(moduleName)
                
            except Exception as e:
                print(f"[ERR] Agent Register: {moduleName}")
                print(repr(e))
                continue

            for name, obj in inspect.getmembers(module, inspect.isclass):
                # print(f"[i] Agent Registry{name}")
                className = obj.__name__
                if hasattr(obj, "metadata") and obj.metadata:
                    # curMetadata = obj.metadata
                    agentsCount +=1
                    agentName = obj.metadata.name
                    agentCapability = obj.metadata.capability
                    
                    self.collection.upsert(
                        ids=[agentName],
                        documents=[f"Agent Name: {agentName}\nCapability: {agentCapability}"],
                        metadatas=[{
                            "name": agentName,
                            "capability": agentCapability,
                            "className": className,
                            "moduleName": moduleName
                        }]
                    )
            
        print(f"[i] Agent Registry: {agentsCount} Agents Founded.")
    
    def query_relevant_agents(
        self, 
        userPrompt: str, 
        maxResults: int = 10,
        scoreThreshold: float = 1.2):
        
        results = self.collection.query(
            query_texts=[userPrompt],
            n_results= maxResults,
        )
        
        print(f"[i] Agent Registry: {results} ")
        
        relevantAgents = []
        if not results and not results['ids'] and len(results['ids'][0]) < 1:
            return relevantAgents
        
        for i in range(len(results["ids"][0])):
            agentID = results["ids"][0][i]
            distanceScore = results["distances"][0][i] if "distances" in results and results["distances"] else 0
            metadata = results["metadatas"][0][i]
            
            if distanceScore < scoreThreshold :
                relevantAgents.append(metadata)
        
        return relevantAgents
    
    def getAgentClass(self, nodeName: str):
        if not nodeName:
            raise ValueError("[ERR] PlannerNode - Agent Registry: Node Name not found ")
        
        result = self.collection.get(
        ids=[nodeName],
        include=["metadatas"]
    )

        if not result["ids"]:
            raise ValueError(f"[ERR] Planner Node - Agent Registry Agent {nodeName} not found")
        
        
        metadata = result["metadatas"][0]
        module = importlib.import_module(
            metadata["moduleName"]
        )

        return getattr(
            module,
            metadata["className"]
        )    
