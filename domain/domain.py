# BaseModel đảm bảo dữ liệu bước vào domain luôn sạch, đúng kiểu, giảm lỗi vặt khi xử lý logic nghiệp vụ.
from pydantic import BaseModel, field_validator
from typing import List, Union

# loại API nhận vào sẽ là str hoặc list
class ReviewRequest(BaseModel):
    text: Union[str, List[str]]
    
    @field_validator("text", mode="before")
    @classmethod
    def _coerce(cls, v):
        if isinstance(v, str):
            return v
        if isinstance(v, (list, tuple)):
            return [str(t) for t in v]
        raise TypeError("text must be str or list[str]")

    def as_list(self) -> List[str]:
        return [self.text] if isinstance(self.text, str) else [t for t in self.text if t and t.strip()]

class ReviewResponse(BaseModel):
    sentiment: str
    score: float | None = None
