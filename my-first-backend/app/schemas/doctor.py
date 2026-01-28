from typing import Optional
from pydantic import BaseModel, Field


class Doctor(BaseModel):
    id: int = Field(..., title="医生ID", description="医生唯一标识")
    name: str = Field(..., title="姓名", description="医生姓名")
    gender: Optional[str] = Field(None, title="性别", description="医生性别")
    department: Optional[str] = Field(None, title="科室", description="所属科室")
    title: Optional[str] = Field(None, title="职称", description="医生职称")
    phone: Optional[str] = Field(None, title="电话", description="联系电话")
    email: Optional[str] = Field(None, title="邮箱", description="电子邮箱")
    office: Optional[str] = Field(None, title="办公室", description="办公室位置")
    hire_date: Optional[str] = Field(None, title="入职日期", description="YYYY-MM-DD")
    created_at: str = Field(..., title="创建时间", description="创建时间 ISO 格式")


class CreateDoctor(BaseModel):
    name: str = Field(..., title="姓名", description="医生姓名")
    gender: Optional[str] = Field(None, title="性别", description="医生性别")
    department: Optional[str] = Field(None, title="科室", description="所属科室")
    title: Optional[str] = Field(None, title="职称", description="医生职称")
    phone: Optional[str] = Field(None, title="电话", description="联系电话")
    email: Optional[str] = Field(None, title="邮箱", description="电子邮箱")
    office: Optional[str] = Field(None, title="办公室", description="办公室位置")
    hire_date: Optional[str] = Field(None, title="入职日期", description="YYYY-MM-DD")


class UpdateDoctor(BaseModel):
    name: Optional[str] = Field(None, title="姓名", description="医生姓名")
    gender: Optional[str] = Field(None, title="性别", description="医生性别")
    department: Optional[str] = Field(None, title="科室", description="所属科室")
    title: Optional[str] = Field(None, title="职称", description="医生职称")
    phone: Optional[str] = Field(None, title="电话", description="联系电话")
    email: Optional[str] = Field(None, title="邮箱", description="电子邮箱")
    office: Optional[str] = Field(None, title="办公室", description="办公室位置")
    hire_date: Optional[str] = Field(None, title="入职日期", description="YYYY-MM-DD")
