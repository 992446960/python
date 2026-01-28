from datetime import datetime
from typing import Optional
from app.db import get_connection
from contextlib import contextmanager

@contextmanager
def _get_db_connection():
    """数据库连接上下文管理器，确保连接正确关闭"""
    conn = get_connection()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _row_to_dict(row) -> dict:
    return dict(row) if row is not None else None


def create_user(data: dict) -> dict:
    """
    创建用户并返回刚插入的用户记录

    :param data: 包含用户信息的字典，例如：
        {
            "name": "Tom",
            "email": "tom@example.com",
            "phone": "123456",
            "role": "admin"
        }
    :return: 数据库中真实存在的用户记录（dict）
    """

    # 1️⃣ 获取数据库连接
    # conn 表示一次数据库会话，用于执行 SQL、提交事务
    with _get_db_connection() as conn:

        cur = conn.cursor()

    # 3️⃣ 执行 INSERT 语句，将用户数据写入 users 表
    # 使用 ? 占位符进行参数绑定，防止 SQL 注入
    # 注意：
    # - 显式写出字段名，避免字段顺序变化带来的问题
    # - created_at 使用 UTC 时间，避免时区混乱
        cur.execute(
            """
            INSERT INTO users (name, email, phone, role, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                data.get("name"),  # 用户名（NOT NULL，建议在上层校验）
                data.get("email"),  # 邮箱（可为 NULL）
                data.get("phone"),  # 手机号（可为 NULL）
                data.get("role"),  # 角色（可为 NULL）
                1,  # 用户状态，1 表示启用
                datetime.utcnow().isoformat(),  # 创建时间（ISO 格式字符串）
            ),
        )

    # 4️⃣ 获取刚刚插入记录的自增主键 ID
    # lastrowid 是当前连接中最后一次 INSERT 生成的主键
        user_id = cur.lastrowid

    # 5️⃣ 使用主键 ID 查询刚插入的用户记录
    # 这样可以保证返回的是数据库中“真实存在”的数据
        cur.execute(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),  # 注意这里是单元素元组，必须加逗号
        )

    # 6️⃣ 获取查询结果的一行数据
    # 前提需要设置conn.row_factory = sqlite3.Row
    # fetchone() 返回的是 Row / tuple，这里转成 dict 方便上层使用
        row = _row_to_dict(cur.fetchone())

    # 7️⃣ 提交事务
    # 如果不 commit，INSERT 的数据可能不会真正写入数据库
        conn.commit()

    # 8 返回新创建的用户数据
        return row


def list_users(
    limit: int,
    offset: int,
    name: str | None = None,
    role: str | None = None,
    email: str | None = None,
    phone: str | None = None,
) -> tuple[list[dict], int]:
    """
    分页查询用户列表，支持多条件筛选
    
    :param limit: 每页数量
    :param offset: 偏移量
    :param name: 姓名模糊匹配
    :param role: 角色精确匹配
    :param email: 邮箱精确匹配
    :param phone: 手机号精确匹配
    :return: (用户列表, 总记录数)
    """
    with _get_db_connection() as conn:
        cur = conn.cursor()
        # 1) 动态拼接 WHERE 条件    
        filters = []
        params = []
        if name:
            filters.append("name LIKE ?")
            params.append(f"%{name}%")
        if role:
            filters.append("role = ?")
            params.append(role)
        if email:
            filters.append("email = ?")
            params.append(email)
        if phone:
            filters.append("phone = ?")
            params.append(phone)

        where_sql = f" WHERE {' AND '.join(filters)}" if filters else ""
        # 2) 先查总数
        cur.execute(f"SELECT COUNT(1) FROM users{where_sql}", params)
        total = int(cur.fetchone()[0])

        # 3) 再查分页数据
        cur.execute(
            f"SELECT * FROM users{where_sql} ORDER BY id DESC LIMIT ? OFFSET ?",
         params + [limit, offset],
        )
        rows = [dict(row) for row in cur.fetchall()]

        return rows, total


def get_user_by_id(user_id: int) -> Optional[dict]:
    # 按照主键查询
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    row = _row_to_dict(cur.fetchone())
    conn.close()
    return row


def update_user(user_id: int, data: dict) -> Optional[dict]:
    # 修改用户
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        existing = cur.fetchone()
        if not existing:
            conn.close()
            return None
        fields = []
        params = []
        for field, value in data.items():
            if value is not None:
                fields.append(f"{field}=?")
                params.append(value)
        if not fields:
            return _row_to_dict(existing)

        params.append(user_id)
        cur.execute(f"UPDATE users SET {', '.join(fields)} WHERE id = ?", params)

        # 查询更新后的数据
        cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = dict(cur.fetchone())

        conn.commit()
        conn.close()
        return row
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def delete_user(user_id: int) -> bool:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    delete = cur.rowcount > 0
    conn.commit()
    conn.close()
    return delete
