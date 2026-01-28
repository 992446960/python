from datetime import datetime
from typing import Optional
from app.db import get_connection


def _row_to_dict(row) -> dict:
    # sqlite3.Row -> dict，便于业务层使用
    return dict(row) if row is not None else None


def create_patient(data: dict) -> dict:
    # 写入患者数据并返回新纪录
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO patients (
            name, gender, date_of_birth, phone, id_card, address, emergency_contact,
            primary_doctor_id, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            data.get("name"),
            data.get("gender"),
            data.get("date_of_birth"),
            data.get("phone"),
            data.get("id_card"),
            data.get("address"),
            data.get("emergency_contact"),
            data.get("primary_doctor_id"),
            datetime.utcnow().isoformat(),
        ),
    )
    patient_id = cur.lastrowid
    # 回查刚插入的数据，保持返回结构一致
    cur.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = _row_to_dict(cur.fetchone())
    conn.commit()
    conn.close()
    return row


def list_patients(limit: int, offset: int) -> tuple[list[dict], int]:
    # 分页返回患者列表
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(1) FROM patients")
    total = int(cur.fetchone()[0])
    cur.execute(
        "SELECT * FROM patients ORDER BY id DESC LIMIT ? OFFSET ?",
        (limit, offset),
    )
    rows = [dict(row) for row in cur.fetchall()]
    conn.close()
    return rows, total


def get_patient_by_id(patient_id: int) -> Optional[dict]:
    # 按主键查询
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = _row_to_dict(cur.fetchone())
    conn.close()
    return row


def update_patient(patient_id: int, data: dict) -> Optional[dict]:
    # 局部更新：只更新请求中提供的字段
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    existing = cur.fetchone()
    if not existing:
        conn.close()
        return None

    fields = []
    params = []
    for field in (
        "name",
        "gender",
        "date_of_birth",
        "phone",
        "id_card",
        "address",
        "emergency_contact",
        "primary_doctor_id",
    ):
        if data.get(field) is not None:
            fields.append(f"{field} = ?")
            params.append(data.get(field))

    if fields:
        # 只更新提供的字段，避免覆盖为 NULL
        params.append(patient_id)
        cur.execute(f"UPDATE patients SET {', '.join(fields)} WHERE id = ?", params)

    cur.execute("SELECT * FROM patients WHERE id = ?", (patient_id,))
    row = _row_to_dict(cur.fetchone())
    conn.commit()
    conn.close()
    return row


def delete_patient(patient_id: int) -> bool:
    # 返回是否成功删除
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM patients WHERE id = ?", (patient_id,))
    deleted = cur.rowcount > 0
    conn.commit()
    conn.close()
    return deleted
