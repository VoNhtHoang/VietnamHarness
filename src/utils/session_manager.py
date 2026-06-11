# 1st Libs
import json
from pathlib import Path
from datetime import datetime


# 3rd Libs


# Insource


# ====================== SOURCE =======================
_SESSIONS_META_PATH = "sessions_meta.json"
# class SessionManager:
#     def __init__(self):
#         pass

def _load_session_meta(self):
    if not Path.exists(_SESSIONS_META_PATH):
        return {}
    
    with open(_SESSIONS_META_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_session_meta(meta_data):
    with open(_SESSIONS_META_PATH, "w", encoding="utf-8") as f:
        json.dump(meta_data, f, indent=2, ensure_ascii=False)

def update_session_meta(session_id, first_prompt):
    """Tự động tạo tiêu đề ngắn gọn dựa trên prompt đầu tiên của user"""
    meta = _load_session_meta()
    
    # Nếu session chưa có tiêu đề, lấy 40 ký tự đầu của prompt làm tiêu đề tạm thời
    if session_id not in meta:
        title = first_prompt[:40] + "..." if len(first_prompt) > 40 else first_prompt
        meta[session_id] = {
            "title": title,
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        meta[session_id]["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
    _save_session_meta(meta)
    
def list_sessions():
    """ In ra danh sách các session hiện có cho người dùng chọn """
    meta = _load_session_meta()
    if not meta:
        print("\n Chưa có phiên làm việc (session) nào được tạo.")
        return

    print("\n" + "="*70)
    print(f"{'SESSION ID':<15} | {'CỰU CẢNH / TIÊU ĐỀ':<35} | {'CẬP NHẬT CUỐI':<15}")
    print("="*70)
    for s_id, info in meta.items():
        print(f"{s_id:<15} | {info['title']:<35} | {info['updated_at']:<15}")
    print("="*70)
    print("Chạy lệnh: python main.py <session_id> để khôi phục phiên làm việc!")