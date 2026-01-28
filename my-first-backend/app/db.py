import sqlite3
from pathlib import Path

# 数据库文件路径：指向项目根目录下的 clinic.db
DB_PATH = Path(__file__).resolve().parent.parent / "clinic.db"


def get_connection():
    # 建立 SQLite 连接
    conn = sqlite3.connect(DB_PATH)
    # 将查询结果映射成字典样式，便于序列化
    conn.row_factory = sqlite3.Row
    # SQLite 默认不启用外键，这里显式开启
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def _get_user_version(conn: sqlite3.Connection) -> int:
    # 读取数据库的迁移版本号
    cur = conn.cursor()
    cur.execute("PRAGMA user_version")
    return int(cur.fetchone()[0])


def _set_user_version(conn: sqlite3.Connection, version: int) -> None:
    # 设置数据库的迁移版本号
    cur = conn.cursor()
    cur.execute(f"PRAGMA user_version = {version}")


def _migration_1(conn: sqlite3.Connection) -> None:
    # 版本1：创建医生/患者表 + 必要索引与唯一约束
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT,
            department TEXT,
            title TEXT,
            phone TEXT,
            email TEXT,
            office TEXT,
            hire_date TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            gender TEXT,
            date_of_birth TEXT,
            phone TEXT,
            id_card TEXT,
            address TEXT,
            emergency_contact TEXT,
            primary_doctor_id INTEGER,
            created_at TEXT NOT NULL,
            FOREIGN KEY (primary_doctor_id) REFERENCES doctors(id)
        )
        """
    )
    # 唯一约束与索引：避免重复数据并提高查询性能
    cur.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_doctors_phone_unique ON doctors(phone)"
    )
    cur.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_doctors_email_unique ON doctors(email)"
    )
    cur.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_patients_phone_unique ON patients(phone)"
    )
    cur.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_patients_id_card_unique ON patients(id_card)"
    )
    cur.execute(
        "CREATE INDEX IF NOT EXISTS idx_patients_primary_doctor ON patients(primary_doctor_id)"
    )

def _migration_2(conn:sqlite3.Connection) -> None:
    # 版本2：创建 users 表
    cur = conn.cursor()
    cur.execute(
          """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            role TEXT,
            status INTEGER NOT NULL DEFAULT 1,
            created_at TEXT NOT NULL
        )
        """
    )
     # 唯一索引：防止 email/phone 重复
    cur.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email_unique ON users(email)"
    )
    cur.execute(
        "CREATE UNIQUE INDEX IF NOT EXISTS idx_users_phone_unique ON users(phone)"
    )

def init_db():
    # 初始化数据库（按版本执行迁移）
    conn = get_connection()
    try:
        version = _get_user_version(conn)
        if version < 1:
            _migration_1(conn)
            _set_user_version(conn, 1)
        if version < 2:
            _migration_2(conn)
            _set_user_version(conn, 2)
        conn.commit()
    finally:
        conn.close()
