# 1rd Libs
import json

# 3rd Libs

# Insource
from src.graph.graph import workflow

if __name__ == '__main__':
    userPrompt = "Tạo cho tôi cái web app đơn giản"
    
    result = workflow.invoke({"userPrompt": userPrompt},
                             {"recursion_limit": 100})
    
    print(f"[AI] {result["resMessages"][-1].content}")
    
    print(json.dumps(result["currentPlan"], indent=2, ensure_ascii=False))    
    