import sqlite3
from app.schemas.doctor import Doctor, CreateDoctor, UpdateDoctor
from app.schemas.user import ApiResponse, ErrorCode
from app.repositories import doctor_repo


def _to_dict(model):
    # 兼容 Pydantic v1/v2 的序列化方法
    return model.model_dump() if hasattr(model, "model_dump") else model.dict()


def list_doctors_service():
    # 返回医生列表
    doctors = [Doctor(**row) for row in doctor_repo.list_doctors()]
    return ApiResponse.success(doctors)


def get_doctor_by_id_service(doctor_id: int):
    # 查询单个医生
    row = doctor_repo.get_doctor_by_id(doctor_id)
    if not row:
        return ApiResponse.error(code=ErrorCode.NOT_FOUND, msg="doctor not found")
    return ApiResponse.success(Doctor(**row))


def create_doctor_service(payload: CreateDoctor):
    # 创建医生并统一错误处理
    try:
        row = doctor_repo.create_doctor(_to_dict(payload))
        return ApiResponse.success(Doctor(**row))
    except sqlite3.IntegrityError:
        # Unique constraint conflicts land here.
        return ApiResponse.error(code=ErrorCode.PARAM_ERROR, msg="doctor data conflict")
    except Exception:
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="create doctor failed")


def update_doctor_service(doctor_id: int, payload: UpdateDoctor):
    # 更新医生并统一错误处理
    try:
        row = doctor_repo.update_doctor(doctor_id, _to_dict(payload))
        if not row:
            return ApiResponse.error(code=ErrorCode.NOT_FOUND, msg="doctor not found")
        return ApiResponse.success(Doctor(**row))
    except sqlite3.IntegrityError:
        return ApiResponse.error(code=ErrorCode.PARAM_ERROR, msg="doctor data conflict")
    except Exception:
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="update doctor failed")


def delete_doctor_service(doctor_id: int):
    # 删除医生并统一错误处理
    try:
        deleted = doctor_repo.delete_doctor(doctor_id)
        if not deleted:
            return ApiResponse.error(code=ErrorCode.NOT_FOUND, msg="doctor not found")
        return ApiResponse.success(None)
    except Exception:
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="delete doctor failed")
