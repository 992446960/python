from fastapi import APIRouter, Query, Header, Depends
from app.schemas.user import (
    User,
    CreateUser,
    UpdateUser,
    ApiResponse,
    PageResult,
    PageParams,
    PageResponse,
)
from app.services.user import (
    get_user_by_id_service,
    get_all_users,
    create_user_service,
    update_user_service,
    delete_user_service,
)

router = APIRouter(prefix="/users", tags=["用户管理"])


# 获取用户列表
@router.get(
    "",
    summary="查询用户列表",
    description="分页查询用户列表，支持角色筛选",
    response_model=ApiResponse[PageResponse[User]],
)
def get_users(
    authorization: str = Header(None, description="登录令牌，格式：Bearer <token>"),
    page: PageParams = Depends(),
    name: str | None = Query(None, description="用户姓名"),
    role: str | None = Query(None, description="用户角色"),
    email: str | None = Query(None, description="用户邮箱"),
    phone: str | None = Query(None, description="用户手机号"),
):
    return get_all_users(page, name, role, email, phone)


# 通过id获取用户详情
@router.get("/{id}", summary="用户详情", response_model=ApiResponse[User])
def get_user_by_id(id: int):
    return get_user_by_id_service(id)


# 新增用户
@router.post("", summary="新增用户", response_model=ApiResponse[User])
def create_user(user: CreateUser):
    return create_user_service(user)


# 修改用户
@router.put("/{id}", summary="修改用户", response_model=ApiResponse[User])
def update_user(id: int, user: UpdateUser):
    return update_user_service(id, user)


# 删除用户
@router.delete("/{id}", summary="删除用户", response_model=ApiResponse[None])
def delete_user(id: int):
    return delete_user_service(id)
