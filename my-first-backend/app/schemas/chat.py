from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, Any
from uuid import UUID, uuid4


class ChatRequest(BaseModel):
    """聊天请求参数"""
    model_config = ConfigDict(protected_namespaces=())
    
    user_input: str = Field(..., description="用户输入内容")
    business_scenario: str = Field(..., description="业务场景")
    conversation_id: str = Field(..., description="会话ID，UUID格式")
    model_id: int = Field(..., description="模型ID")
    prompt_id: int = Field(..., description="提示词ID")
    user_role: Literal["patient", "doctor"] = Field(..., description="用户角色")


class SSEEventData(BaseModel):
    """SSE 事件数据基类"""
    event: Literal["start", "ping", "delta", "tool", "final", "error"]
    conversation_id: str
    request_id: str
    data: Optional[Any] = None


class DeltaData(BaseModel):
    """delta 事件的数据结构"""
    content: str = Field("", description="内容")
    thinking_content: str = Field("", description="思考内容")
    tool_calls: Optional[Any] = None


class FinalData(BaseModel):
    """final 事件的数据结构"""
    result_type: Literal["text", "tool"] = Field(..., description="结果类型")
    text: str = Field("", description="文本内容")
    data: Optional[Any] = None


class ToolOutputFile(BaseModel):
    """文件信息"""
    file_name: str
    file_id: str
    file_url: Optional[str] = None
    file_type: Optional[str] = None


class DiagnosisItem(BaseModel):
    """诊断项"""
    item: str
    file_list: list[ToolOutputFile] = []


class ExamItem(BaseModel):
    """检查项"""
    item: str
    file_list: list[ToolOutputFile] = []


class TreatmentItem(BaseModel):
    """治疗项"""
    item: str
    file_list: list[ToolOutputFile] = []


class DigitalDoctorReasoningOutput(BaseModel):
    """数字医生推理输出"""
    diagnosis: dict = Field(default_factory=lambda: {"list": []})
    exams: dict = Field(default_factory=lambda: {"list": []})
    treatments: dict = Field(default_factory=lambda: {"list": []})


class EvidenceConclusionOutput(BaseModel):
    """证据结论输出"""
    evidence_list: list[dict] = []


class PersonalizedAnalysisOutput(BaseModel):
    """个性化分析输出"""
    record_list: list[dict] = []


class ToolData(BaseModel):
    """tool 事件的数据结构"""
    tool_name: Literal[
        "digital_doctor_reasoning",
        "evidence_conclusion",
        "personalized_analysis",
        "integrated_reasoning"
    ]
    tool_output: dict