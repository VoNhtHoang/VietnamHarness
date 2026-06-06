# 1st Libs
from typing import List
from pydantic import BaseModel, Field

# 3rd Libs

# 
class File(BaseModel):
    path : str = Field(description=  "Đường dẫn dến file cần tạo / chỉnh sửa.")
    description: str = Field( description="Mục đích tồn tại của file" )
    

class SubTask(BaseModel):
    description : str = Field(
        description="Mô tả chi tiết về nhiệm vụ cần được hoàn thành, mỗi chi tiết nhiệm vụ nhỏ hơn sẽ được liệt kê trên các hàng để các agent khác có thể sử dụng và thực thi."
        )
    file: File = Field(description="File được tạo / chỉnh sửa trong sub-task này.")
    
class SubTaskList(BaseModel):
    subTasks: List[SubTask] = Field(description="Danh sách các sub-task cần phải hoàn thành cho nhiệm vụ")