# 1 st Libs
from typing import List
from pydantic import BaseModel, Field

# 3rd Libss

# Insource
from src.agents.init_base import File


# ================  SOURCE   ===============

class TestFileSpecification(BaseModel):
    testFilePath: str = Field(
        description="Đường dẫn của file test cần được tạo mới hoặc chỉnh sửa (Ví dụ: 'tests/test_auth.py')."
    )
    targetFile: File = Field(
        description="File mã nguồn gốc mà file test này đang nhắm tới để kiểm thử."
    )
    testCasesDescription: str = Field(
        description="Mô tả chi tiết các kịch bản/test case cần viết bên trong file (Ví dụ: 'Test login thành công', 'Test sai mật khẩu')."
    )

class TestExecutionPlan(BaseModel):
    testFiles: List[TestFileSpecification] = Field(description = "Danh sách các file test cần được xây dựng.")
    runCommand: str = Field (
        description = "Câu lệnh Terminal hoàn chỉnh để execute các bài kiểm thử này (Ví dụ: 'pytest tests/test_auth.py' hoặc 'npm test'), nếu có nhiều câu lệnh, hãy ngăn cách bằng ';'."
    )
    
    
class TestAgentMetaData(BaseModel):
    name: str = Field(
        default="test_automation_agent", 
        description="Tên định danh bắt buộc để Planner nhận diện Node."
    )
    capability: str = Field(
        default=(
            "Chuyên phân tích mã nguồn và các tệp tin được tạo/chỉnh sửa để tự động sinh ra "
            "các kịch bản kiểm thử (Unit test, Integration test). Tự tạo cấu trúc file test "
            "và cung cấp lệnh chạy test tự động trên hệ thống."
        ),
        description="Năng lực chi tiết được lưu vào VectorDB để PlannerNode tìm kiếm."
    )

class TestAgentNode:
    """
    Một node (agent) có thể được dùng trong LangGraph, có chức năng tạo các trường hợp test và thực thi các cậu lệnh dựa trên modified system files để test mã nguồn.
    """
    
    def __init__(self, llm):
        self.llm = llm
        self.metadata = TestAgentMetaData()
        self.system_prompt = (
            "Bạn là một Kỹ sư Kiểm thử Phần mềm Tự động (QA Automation Engineer) cấp cao. "
            "Nhiệm vụ của bạn là đọc danh sách các file mã nguồn được cung cấp, hiểu mục đích của chúng, "
            "và thiết kế ra một kế hoạch viết test toàn diện bao gồm: các file test cần tạo, "
            "mô tả các test case chi tiết bên trong, và câu lệnh chính xác để chạy bộ test đó."
        )
        
    def call(self, state: dict) -> dict:
        """
        Hàm thực thi chính của Node bên trong đồ thị LangGraph.
        """
        modified_files = state.get("modified_files", [])
        user_requirement = state.get("user_prompt", "")
        
        if not modified_files:
            context_input = f"Yêu cầu hệ thống: {user_requirement}"
        else:
            context_input = f"Yêu cầu: {user_requirement}\nDanh sách các file cần viết test:\n"
            for file in modified_files:
                context_input += f"- File: {file.get('path')} | Mô tả: {file.get('description')}\n"

        structured_llm = self.llm.with_structured_output(TestExecutionPlan)
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Hãy lên kế hoạch kiểm thử cho thông tin sau:\n{context_input}"}
        ]
        
        test_plan: TestExecutionPlan = structured_llm.invoke(messages)
        
        return {
            "test_specs": test_plan.model_dump()["test_files"],
            "test_run_command": test_plan.model_dump()["run_command"]
        }
    