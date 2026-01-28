from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    """应用配置"""
    # 数据库配置
    db_path: str = str(Path(__file__).parent.parent / "clinic.db")
    
    # API 配置
    api_title: str = "Clinic Management API"
    api_version: str = "1.0.0"
    api_prefix: str = "/api/v1"
    
    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"
    
    # 分页配置
    default_page_size: int = 10
    max_page_size: int = 100
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()