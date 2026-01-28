from pydantic import BaseModel, Field, field_validator , EmailStr
from typing import Generic, TypeVar, Optional
import re

T = TypeVar("T")


class PageParams(BaseModel):
    pageNum: int = Field(1, title="页码", description="当前页码")
    pageSize: int = Field(10, title="每页数量", description="每页返回的数据条数")

class BusinessCode:
    """
    业务错误码定义
    """
   # 成功
    SUCCESS = 200        # OK: 请求成功
    CREATED = 201        # Created: 创建资源成功

    # 客户端错误 (4xx)
    PARAM_ERROR = 400    # Bad Request: 参数校验失败、语义错误
    UNAUTHORIZED = 401   # Unauthorized: 未登录/Token无效
    FORBIDDEN = 403      # Forbidden: 已登录但无权访问（你之前用的1004不符合标准）
    NOT_FOUND = 404      # Not Found: 资源不存在

    # 服务端错误 (5xx)
    INTERNAL_ERROR = 500 # Internal Server Error: 服务器内部崩溃或代码逻辑错误
    GATEWAY_ERROR = 502  # Bad Gateway: 网关或上游服务异常

class ErrorCode:
    """
    具体业务错误码定义
    """
    # 客户端错误 (4xx)
    PARAM_ERROR = 400    # Bad Request: 参数校验失败、语义错误
    UNAUTHORIZED = 401   # Unauthorized: 未登录/Token无效
    FORBIDDEN = 403      # Forbidden: 已登录但无权访问（你之前用的1004不符合标准）
    NOT_FOUND = 404      # Not Found: 资源不存在

    # 服务端错误 (5xx)
    INTERNAL_ERROR = 500 # Internal Server Error: 服务器内部崩溃或代码逻辑错误
    GATEWAY_ERROR = 502  # Bad Gateway: 网关或上游服务异常


class ApiResponse(BaseModel, Generic[T]):
    """
    统一接口响应结构
    """
    code: int = Field(..., title="业务状态码", description="业务状态码，200 表示成功，非 200 表示业务错误")
    msg: str = Field(..., title="消息", description="消息")
    data: Optional[T] = None

    @classmethod
    def success(cls, data: Optional[T] = None, msg: str = "success"):
        return cls(code=200, msg=msg, data=data)

    @classmethod
    def error(cls, code: int, msg: str):
        return cls(code=code, msg=msg, data=None)


class User(BaseModel):
    id: int = Field(..., title="用户ID", description="用户的唯一标识，用于区分不同用户")
    name: str = Field(..., title="用户名", description="用户的显示名称")
    email: Optional[str] = Field(None, title="邮箱")
    phone: Optional[str] = Field(None, title="手机")
    role: str = Field(None, title="用户角色", description="用户在系统中的角色标识")
    status: int = Field(..., title="状态")
    created_at: str = Field(..., title="创建时间")


class CreateUser(BaseModel):
    name: str = Field(..., title="用户名",description="用户名")
    email: str = Field(..., title="邮箱",description="邮箱")
    phone: str = Field(..., title="手机",description="手机")
    role: str = Field(..., title="角色",description="角色")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v: str) -> str:
        """验证邮箱格式"""
        if not v or not v.strip():
            raise ValueError('邮箱不能为空')
        # 简单的邮箱格式验证
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, v.strip()):
            raise ValueError('邮箱格式不正确')
        return v.strip().lower()
    
    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v: str) -> str:
        """验证手机号格式（支持11位数字）"""
        if not v or not v.strip():
            raise ValueError('手机号不能为空')
        phone = v.strip().replace('-', '').replace(' ', '')
        if not phone.isdigit() or len(phone) != 11:
            raise ValueError('手机号必须是11位数字')
        return phone
    
    @field_validator('name', 'role')
    @classmethod
    def validate_not_empty(cls, v: str) -> str:
        """验证非空且去除首尾空格"""
        if not v or not v.strip():
            raise ValueError('字段不能为空或仅包含空格')
        return v.strip()


class UpdateUser(BaseModel):
    name: Optional[str] = Field(None, title="用户名")
    email: Optional[str] = Field(None, title="邮箱")
    phone: Optional[str] = Field(None, title="手机")
    role: Optional[str] = Field(None, title="角色")
    status: Optional[int] = Field(None, title="状态")


class PageResult(BaseModel, Generic[T]):
    """
    基础分页结果（不包含请求参数）
    """

    total: int = Field(..., title="总记录数量", description="符合条件的总数据量")
    rows: list[T] = Field(..., title="列表数据", description="当前页的数据列表")


class PageResponse(PageParams, Generic[T]):
    """
    分页响应模型（继承分页请求参数）
    包含：pageNum / pageSize / total / rows
    """

    total: int = Field(..., title="总记录数量", description="符合条件的总数据量")
    rows: list[T] = Field(..., title="列表数据", description="当前页的数据列表")
