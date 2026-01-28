import sqlite3
import logging
from app.schemas.user import (
    User,
    UpdateUser,
    CreateUser,
    ApiResponse,
    PageResult,
    PageParams,
    PageResponse,
    ErrorCode,
)
from app.repositories import user_repo
# 配置日志
logger = logging.getLogger(__name__)

def _to_dict(model):
    # 兼容 Pydantic v1/v2 的序列化方法
    return model.model_dump() if hasattr(model, "model_dump") else model.dict()


def get_all_users(
    page: PageParams = PageParams(),
    name: str | None = None,
    role: str | None = None,
    email: str | None = None,
    phone: str | None = None,
):
    try:
        limit = page.pageSize
        offset = (page.pageNum - 1) * page.pageSize

        rows, total = user_repo.list_users(
            limit=limit,
            offset=offset,
            name=name,
            role=role,
            email=email,
            phone=phone,
        )

        users = [User(**row) for row in rows]

        return ApiResponse.success(
            PageResponse[User](
                pageNum=page.pageNum,
                pageSize=page.pageSize,
                total=total,
                rows=users,
            )
        )
    except Exception as e:
        logger.error(f"获取用户列表失败: {str(e)}", exc_info=True)
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="获取用户列表失败")


def get_user_by_id_service(id: int):
    try:
        row = user_repo.get_user_by_id(id)
        if not row:
            return ApiResponse.error(code=ErrorCode.NOT_FOUND, msg="用户不存在")
        return ApiResponse.success(User(**row))
    except Exception as e:
        logger.error(f"获取用户详情失败 [id={id}]: {str(e)}", exc_info=True)
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="获取用户详情失败")



def create_user_service(user: CreateUser):
    try:
        new_user = user_repo.create_user(_to_dict(user))
        logger.info(f"创建用户成功 [id={new_user['id']}, name={new_user['name']}]")
        return ApiResponse.success(User(**new_user))

    except sqlite3.IntegrityError as e:
        logger.warning(f"创建用户失败，数据冲突: {str(e)}")
        # Unique constraint conflicts land here.
        return ApiResponse.error(code=ErrorCode.PARAM_ERROR, msg="用户数据冲突，邮箱或手机号已存在")
    except Exception as e:
        logger.error(f"创建用户失败: {str(e)}", exc_info=True)
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="创建用户失败")


def update_user_service(id: int, user: UpdateUser):
    try:
        update_data = {k:v for k,v in _to_dict(user).items() if v is not None}
        if not update_data:
            return ApiResponse.error(code=ErrorCode.PARAM_ERROR, msg="没有要更新的字段")
        row = user_repo.update_user(id,update_data)
        if not row:
            return ApiResponse.error(code=ErrorCode.NOT_FOUND, msg="用户不存在")
        logger.info(f"更新用户成功 [id={id}]")
        return ApiResponse.success(User(**row))
    except sqlite3.IntegrityError as e:
        logger.warning(f"更新用户失败，数据冲突 [id={id}]: {str(e)}")
        return ApiResponse.error(code=ErrorCode.PARAM_ERROR, msg="用户数据冲突")
    except Exception as e:
        logger.error(f"更新用户失败 [id={id}]: {str(e)}", exc_info=True)
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="更新用户失败")

def delete_user_service(id: int):
    try:
        deleted = user_repo.delete_user(id)
        if not deleted:
            return ApiResponse.error(code=ErrorCode.NOT_FOUND, msg="用户不存在")
        logger.info(f"删除用户成功 [id={id}]")
        return ApiResponse.success(None)
    except Exception as e:
        logger.error(f"删除用户失败 [id={id}]: {str(e)}", exc_info=True)
        return ApiResponse.error(code=ErrorCode.INTERNAL_ERROR, msg="删除用户失败")