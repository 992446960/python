from datetime import datetime
from typing import Optional
from app.db import get_connection

# TODO：// 不能复用吗？
def _row_to_dict(row) -> dict:
    # sqlite3.Row -> dict，便于业务层使用
    return dict(row) if row is not None else None


def create_doctor(data: dict) -> dict:
    # 写入医生数据并返回新纪录
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO doctors (
            name, gender, department, title, phone, email, office, hire_date, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("name"),
            data.get("gender"),
            data.get("department"),
            data.get("title"),
            data.get("phone"),
            data.get("email"),
            data.get("office"),
            data.get("hire_date"),
            datetime.utcnow().isoformat(),
        ),
    )
    doctor_id = cur.lastrowid
    # 回查刚插入的数据，保持返回结构一致
    cur.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
    row = _row_to_dict(cur.fetchone())
    conn.commit()
    conn.close()
    return row


def list_doctors() -> list[dict]:
    # 按时间倒序返回医生列表
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors ORDER BY id DESC")
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows


def get_doctor_by_id(doctor_id: int) -> Optional[dict]:
    # 按主键查询
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
    row = _row_to_dict(cur.fetchone())
    conn.close()
    return row


def update_doctor(doctor_id: int, data: dict) -> Optional[dict]:
    # 局部更新：只更新请求中提供的字段
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
    existing = cur.fetchone()
    if not existing:
        conn.close()
        return None

    fields = []
    params = []
    for field in (
        "name",
        "gender",
        "department",
        "title",
        "phone",
        "email",
        "office",
        "hire_date",
    ):
        if data.get(field) is not None:
            fields.append(f"{field} = ?")
            params.append(data.get(field))

    if fields:
        # 只更新提供的字段，避免覆盖为 NULL
        params.append(doctor_id)
        cur.execute(f"UPDATE doctors SET {', '.join(fields)} WHERE id = ?", params)

    cur.execute("SELECT * FROM doctors WHERE id = ?", (doctor_id,))
    row = _row_to_dict(cur.fetchone())
    conn.commit()
    conn.close()
    return row


def delete_doctor(doctor_id: int) -> bool:
    # 返回是否成功删除
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM doctors WHERE id = ?", (doctor_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
