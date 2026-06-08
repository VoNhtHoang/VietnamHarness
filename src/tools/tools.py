import pathlib
import subprocess

from langchain_core.tools import tool

PROJECT_ROOT= pathlib.Path.cwd() / "/ai_proj"

def safePath(path: str) -> pathlib.Path:
    resolved_root = PROJECT_ROOT.resolve()
    resolved_path = (resolved_root / path).resolve()
    
    # Kiểm tra xem resolved_path có thuộc (hoặc chính là) resolved_root không
    if not resolved_path.is_relative_to(resolved_root):
        raise ValueError("[E] Tools: Có thể là lưu ngoài thư mục gốc của dự án")
        
    return resolved_path

@tool
def writeFile(path: str, content: str) -> str:
    """Lưu nội dung vào file với dường dẫn file nằm trong thư mục gốc của dự án"""
    path = safePath(path)
    path.parent.mkdir(parents=True, exist_ok= True)
    with open(path, "w", encoding='utf-8') as file:
        file.write(content)
    
    return f"[i] TOOLS: Wrote file {path}"

@tool
def readFile(path: str) -> str:
    """Đọc nội dung từ file với dường dẫn file nằm trong thư mục gốc của dự án"""
    path = safePath(path)
    if not path.exists():
        return f"[W] TOOLS: File not found!"
    
    with open(path, "r", encoding='utf-8') as file:
        return file.read()

@tool
def getCurrentDirectory() -> str:
    """Kiểm tra thư mục gốc hiện tại của dự án"""
    return str(PROJECT_ROOT)

@tool
def listFiles(directory: str = ".") -> str:
    """Liệt kê các file tồn tại trong thư mục gốc của dự án"""
    path = safePath(directory)
    if not path.is_dir():
        return f"[W] {path} is not à directory"
    
    files = [str(f.relative_to(PROJECT_ROOT)) for f in path.glob("**/*") if f.is_file()]
    return "\n".join(files) if files else "[i] TOOLS: No file Found."
