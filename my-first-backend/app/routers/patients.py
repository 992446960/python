from fastapi import APIRouter
from app.schemas.patient import Patient, CreatePatient, UpdatePatient
from app.schemas.user import ApiResponse
from app.services.patient import (
    list_patients_service,
    get_patient_by_id_service,
    create_patient_service,
    update_patient_service,
    delete_patient_service,
)

router = APIRouter(prefix="/patients", tags=["患者管理"])


@router.get("", summary="查询患者列表", response_model=ApiResponse[list[Patient]])
def list_patients():
    # 只负责转发到 service 层
    return list_patients_service()


@router.get("/{patient_id}", summary="患者详情", response_model=ApiResponse[Patient])
def get_patient(patient_id: int):
    # path 参数由 FastAPI 自动校验类型
    return get_patient_by_id_service(patient_id)


@router.post("", summary="新增患者", response_model=ApiResponse[Patient])
def create_patient(payload: CreatePatient):
    # body 参数交由 Pydantic 做校验
    return create_patient_service(payload)


@router.put("/{patient_id}", summary="修改患者", response_model=ApiResponse[Patient])
def update_patient(patient_id: int, payload: UpdatePatient):
    # 更新只传入变更字段
    return update_patient_service(patient_id, payload)


@router.delete("/{patient_id}", summary="删除患者", response_model=ApiResponse[None])
def delete_patient(patient_id: int):
    # 删除返回空 data
    return delete_patient_service(patient_id)
