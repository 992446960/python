from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import time
import logging
from app.routers import users, doctors, patients, chat
from app.db import init_db
from app.logger import setup_logger
from app.config import settings
from app.schemas.user import ApiResponse, ErrorCode

logger = setup_logger()

app = FastAPI(
    title="Clinic Management API",
    version="1.0.0",
    description="诊所管理系统 API",
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该指定具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求日志中间件
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"{request.method} {request.url.path}")
    response = await call_next(request)
    process_time = time.time() - start_time
    logger.info(f"请求完成，耗时: {process_time:.3f}s")
    return response

# 全局异常处理
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"未处理的异常: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ApiResponse.error(
            code=ErrorCode.INTERNAL_ERROR,
            msg="服务器内部错误"
        ).model_dump()
    )

@app.on_event("startup")
def startup_event():
    logger.info("应用启动中...")
    init_db()
    logger.info("数据库初始化完成")

@app.on_event("shutdown")
def shutdown_event():
    logger.info("应用关闭中...")

# 注册路由
app.include_router(users.router, prefix=settings.api_prefix)
app.include_router(doctors.router, prefix=settings.api_prefix)
app.include_router(patients.router, prefix=settings.api_prefix)
app.include_router(chat.router, prefix=settings.api_prefix)