from typing import Optional
from pydantic import BaseModel, Field


class Patient(BaseModel):
    id: int = Field(..., title="患者ID", description="患者唯一标识")
    name: str = Field(..., title="姓名", description="患者姓名")
    gender: Optional[str] = Field(None, title="性别", description="患者性别")
    date_of_birth: Optional[str] = Field(None, title="出生日期", description="YYYY-MM-DD")
    phone: Optional[str] = Field(None, title="电话", description="联系电话")
    id_card: Optional[str] = Field(None, title="身份证", description="身份证号码")
    address: Optional[str] = Field(None, title="地址", description="家庭住址")
    emergency_contact: Optional[str] = Field(None, title="紧急联系人", description="紧急联系人")
    primary_doctor_id: Optional[int] = Field(
        None, title="主治医生", description="主治医生ID"
    )
    created_at: str = Field(..., title="创建时间", description="创建时间 ISO 格式")


class CreatePatient(BaseModel):
    name: str = Field(..., title="姓名", description="患者姓名")
    gender: Optional[str] = Field(None, title="性别", description="患者性别")
    date_of_birth: Optional[str] = Field(None, title="出生日期", description="YYYY-MM-DD")
    phone: Optional[str] = Field(None, title="电话", description="联系电话")
    id_card: Optional[str] = Field(None, title="身份证", description="身份证号码")
    address: Optional[str] = Field(None, title="地址", description="家庭住址")
    emergency_contact: Optional[str] = Field(None, title="紧急联系人", description="紧急联系人")
    primary_doctor_id: Optional[int] = Field(
        None, title="主治医生", description="主治医生ID"
    )


class UpdatePatient(BaseModel):
    name: Optional[str] = Field(None, title="姓名", description="患者姓名")
    gender: Optional[str] = Field(None, title="性别", description="患者性别")
    date_of_birth: Optional[str] = Field(None, title="出生日期", description="YYYY-MM-DD")
    phone: Optional[str] = Field(None, title="电话", description="联系电话")
    id_card: Optional[str] = Field(None, title="身份证", description="身份证号码")
    address: Optional[str] = Field(None, title="地址", description="家庭住址")
    emergency_contact: Optional[str] = Field(None, title="紧急联系人", description="紧急联系人")
    primary_doctor_id: Optional[int] = Field(
        None, title="主治医生", description="主治医生ID"
    )
