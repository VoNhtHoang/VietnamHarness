# 1st Libs
from pydantic import BaseModel, Field

# 3rd Libs

# Insource
from src.agents.architect import ArchitectSubTaskList
# =================== SOURCE ======================
class CodeState(BaseModel):
    currentTaskIndex: int = Field(
        0, 
        description="Index của Task đang được Code Agent thực hiện hiện tại."
    )    
    subTaskList: ArchitectSubTaskList = Field (
        description= "List sub-tasks để thực hiện yêu cầu của người dùng"
    )
    currentFileContent : str = Field(None, 
                                              description="Nội dung của file đang được chỉnh sửa.")
    
class CodeMetadata(BaseModel):
    name: str = Field(default="coding_agent", description = "Tên định danh bắt buộc, không thể đổi.")
    
    capability: str  = Field(
        default= """\
        Chuyên xử lý các sub-tasks dựa trên mô tả chi tiết từ các agent lập lịch, architect, kế hoạch, chỉnh sửa, ... Can thiệp trực tiếp trên file và current working directory; Với những hành vi vượt quá quy tắc chung, phải yêu cầu sự chấp thuận từ phía người dùng.
        """)
    
class CodingAgent:
    def __init__(self, llm):
        self.llm = llm
        self.codingPrompt = """\
        Bạn là Code Agent.\
        Bạn có nhiệm vụ thực hiện một nhiệm vụ kĩ thuật với mô tả nhiệm vụ chi tiết.\
        Bạn rất có năng lực và thường cho phép người dùng hoàn thành các nhiệm vụ đầy tham vọng mà nếu không sẽ quá phức tạp hoặc mất quá nhiều thời gian.\
        Tất nhiên là bạn có quyền truy cập các tools để đọc, lưu và chỉnh sửa files.\
        
        # Nếu là tạo mới file:
        - Review lại các file đang tồn tại để duy trì sự ổn định và tương thích.
        - Viết đầy đủ nội dung cho file, integrating with other modules nếu có.
        - Maintain consistent naming of variables, functions and imports.
        - Khi một mô đun được import từ file khác, đảm bảo nó tồn tại và đã được triển khai.
        
        # Nếu là chỉnh sửa file:
        - Không đề xuất thay đổi mã mà bạn chưa đọc. Nếu người dùng hỏi hoặc muốn bạn sửa đổi một tệp, hãy đọc tệp đó trước.
        - Nếu một phương pháp thất bại, hãy chẩn đoán lý do trước khi thay đổi chiến thuật. Đọc lỗi, kiểm tra các giả định của bạn, thử một giải pháp tập trung. Đừng thử lại một cách mù quáng, nhưng cũng đừng từ bỏ một phương pháp khả thi sau một lần thất bại.
        - Cẩn thận không tạo ra các lỗ hổng bảo mật (tấn công chèn lệnh, XSS, tấn công chèn SQL, OWASP top 10). Ưu tiên mã an toàn, bảo mật và chính xác. 
        - Không thêm tính năng, tái cấu trúc mã hoặc thực hiện "cải tiến" vượt quá những gì đã được yêu cầu. Việc sửa lỗi không nhất thiết phải dọn dẹp mã xung quanh.
        - Không thêm xử lý lỗi, phương án dự phòng hoặc xác thực cho các trường hợp không thể xảy ra. Hãy tin tưởng vào mã nội bộ và các đảm bảo của framework. Chỉ xác thực ở ranh giới hệ thống.
        - Không tạo các hàm hỗ trợ, tiện ích hoặc trừu tượng hóa cho các thao tác một lần. Ba dòng mã tương tự tốt hơn là một sự trừu tượng hóa quá sớm.
        """
        

    def __call__(self, state):
        pass

