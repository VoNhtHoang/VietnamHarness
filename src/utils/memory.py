# 1st Libs
import sqlite3

# 3 rd Libs
from langgraph.checkpoint.sqlite import SqliteSaver

class SqliteMemoryManager:
    def __init__(self, dbPath: str = "sessions.db"):
        self.dbPath = dbPath
        self.conn = None
        self.memory = None

    def _connect(self) -> SqliteSaver:
        if self.conn is None:
            self.conn = sqlite3.connect(self.dbPath, check_same_thread=False)
            self.memory = SqliteSaver(self.conn)
            print("=== Đã khởi tạo kết nối SQLite ===")
        return self.memory
    
    def disconnect(self):
        """Hàm ngắt kết nối chủ động"""
        if self.conn:
            try:
                self.conn.close()
            
            except Exception as e:
                print(f"\n[E] Có lỗi xảy ra trong Memory - Context; Sqlite lỗi ngắt kết nối: {e}")
            self.conn = None
            self.memory = None
            print("=== Đã đóng kết nối SQLite an toàn ===")
            