import sqlite3
from app.schemas.patient import Patient, CreatePatient, UpdatePatient 
from app.schemas.user import ApiResponse, ErrorCode, PageParams
from app.repositories import patient_repo


def _to_dict(model):
    # 兼容 Pydantic v1/v2 的序列化方法
    return model.model_dump() if hasattr(model, "model_dump") else model.dict()


def list_patients_service(page: PageParams = PageParams()):
    # 返回患者列表
    limit = page.pageSize
    offset = (page.pageNum - 1) * page.pageSize
    rows, total = patient_repo.list_patients(limit=limit, offset=offset)
    patients = [Patient(**row) for row in rows]
    return ApiResponse.success(patients)


def get_patient_by_id_service(patient_id: int):
    # 查询单个患者
    row = patient_repo.get_patient_by_id(patient_id)
    if not row:
        return ApiResponse.error(code=ErrorCode.NOT_FOUND, msg="patient not found")
    return ApiResponse.success(Patient(**row))


def create_patient_service(payload: CreatePatient):
    # 创建患者并统一错误处理
    try:
        row = patient_repo.create_patient(_to_dict(payload))
        return ApiResponse.success(Patient(**row))
    except sqlite3.IntegrityError:
        # Unique constraint or foreign key failure.
        return ApiResponse.error(code=ErrorCode.PARAM_ERROR, msg="patient data conflict")
    except Exception:
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="create patient failed")


def update_patient_service(patient_id: int, payload: UpdatePatient):
    # 更新患者并统一错误处理
    try:
        row = patient_repo.update_patient(patient_id, _to_dict(payload))
        if not row:
            return ApiResponse.error(code=ErrorCode.NOT_FOUND, msg="patient not found")
        return ApiResponse.success(Patient(**row))
    except sqlite3.IntegrityError:
        return ApiResponse.error(code=ErrorCode.PARAM_ERROR, msg="patient data conflict")
    except Exception:
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="update patient failed")


def delete_patient_service(patient_id: int):
    # 删除患者并统一错误处理
    try:
        deleted = patient_repo.delete_patient(patient_id)
        if not deleted:
            return ApiResponse.error(code=ErrorCode.NOT_FOUND, msg="patient not found")
        return ApiResponse.success(None)
    except Exception:
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="delete patient failed")
