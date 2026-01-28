from fastapi import APIRouter
from app.schemas.doctor import Doctor, CreateDoctor, UpdateDoctor
from app.schemas.user import ApiResponse
from app.services.doctor import (
    list_doctors_service,
    get_doctor_by_id_service,
    create_doctor_service,
    update_doctor_service,
    delete_doctor_service,
)

router = APIRouter(prefix="/doctors", tags=["医生管理"])


@router.get("", summary="查询医生列表", response_model=ApiResponse[list[Doctor]])
def list_doctors():
    # 只负责转发到 service 层
    return list_doctors_service()


@router.get("/{doctor_id}", summary="医生详情", response_model=ApiResponse[Doctor])
def get_doctor(doctor_id: int):
    # path 参数由 FastAPI 自动校验类型
    return get_doctor_by_id_service(doctor_id)


@router.post("", summary="新增医生", response_model=ApiResponse[Doctor])
def create_doctor(payload: CreateDoctor):
    # body 参数交由 Pydantic 做校验
    return create_doctor_service(payload)


@router.put("/{doctor_id}", summary="修改医生", response_model=ApiResponse[Doctor])
def update_doctor(doctor_id: int, payload: UpdateDoctor):
    # 更新只传入变更字段
    return update_doctor_service(doctor_id, payload)


@router.delete("/{doctor_id}", summary="删除医生", response_model=ApiResponse[None])
def delete_doctor(doctor_id: int):
    # 删除返回空 data
    return delete_doctor_service(doctor_id)
