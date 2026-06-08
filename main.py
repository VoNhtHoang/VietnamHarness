# 1rd Libs
import json
import uuid
import sys
import atexit

# 3rd Libs

# Insource
from src.graph.graph import _init_workflow


# ================== SOURCE =========================
def run_session ():
    workflow =  _init_workflow()
    print("=" * 60)
    print("TEST SESSION ACTIVE")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        session_id = sys.argv[1]
        print(f"🔄 Đang khôi phục lại Session cũ: {session_id}")
    else:
        session_id = str(uuid.uuid4())[:8]  # Tạo một ID ngắn gọn dễ nhìn
        print(f"[i] Khởi tạo Session mới. ID của bạn là: {session_id}")
        print("[i] (Để tiếp tục phiên này lần sau, chạy: python main.py <id>)")
        
    config = {
        "configurable": {"thread_id": session_id},
        "recursion_limit": 100
    }
    
    print("-" * 60)
    print("Nhập 'exit' hoặc 'quit' để kết thúc phiên làm việc.")
    print("-" * 60)
    
    while True:
        try:
            userPrompt = input("\n You: ").strip()
            
            if not userPrompt or len(userPrompt) < 1:
                continue
            
            if userPrompt.lower() in ['quit()', 'exit()']:
                print(f"[i] Đã đóng session [{session_id}]")
                break

            result = workflow.invoke(
                {"userMessages": [userPrompt]}, 
                config=config
            )
            
            if "resMessages" in result and result["resMessages"]:
                lastMessage = result["resMessages"][-1]
                
                content = lastMessage.content if hasattr(lastMessage, 'content') else str(lastMessage)
                print(f"\n[AI]: {content}")
            
            else:
                print(f"\n[AI] không có tin nhắn phản hồi")
                
            if "currentPlan" in result and result["currentPlan"]:
                print("\n[AI] [Current Plan Status]:")
                print(json.dumps(result["currentPlan"], indent=2, ensure_ascii=False))
        
        except KeyboardInterrupt:
            print(f"\n[W] Đột ngột ngắt Session [{session_id}]. Dữ liệu đã lưu tạm.")
            break
        except Exception as e:
            print(f"\n[E] Có lỗi xảy ra trong Session: {e}")
            
if __name__ == '__main__':
    # load_dotenv()
    run_session()
#     userPrompt = "Tạo cho tôi cái web app đơn giản"
    
#     result = workflow.invoke({"userPrompt": userPrompt},
#                              {"recursion_limit": 100})
    
#     print(f"[AI] {result["resMessages"][-1].content}")
    
#     print(json.dumps(result["currentPlan"], indent=2, ensure_ascii=False))    
    