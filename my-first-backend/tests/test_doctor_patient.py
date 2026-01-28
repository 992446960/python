import tempfile
import unittest
from pathlib import Path

from app import db
from app.schemas.doctor import CreateDoctor, UpdateDoctor
from app.schemas.patient import CreatePatient, UpdatePatient
from app.services.doctor import (
    create_doctor_service,
    get_doctor_by_id_service,
    update_doctor_service,
    delete_doctor_service,
    list_doctors_service,
)
from app.services.patient import (
    create_patient_service,
    get_patient_by_id_service,
    update_patient_service,
    delete_patient_service,
    list_patients_service,
)


class DoctorPatientCrudTests(unittest.TestCase):
    def setUp(self):
        # 每个测试用独立临时库，避免互相污染
        self.temp_dir = tempfile.TemporaryDirectory()
        db.DB_PATH = Path(self.temp_dir.name) / "test.db"
        db.init_db()

    def tearDown(self):
        # 清理临时文件
        self.temp_dir.cleanup()

    def test_doctor_crud(self):
        # 创建医生
        create_resp = create_doctor_service(
            CreateDoctor(name="Dr. Liu", phone="13000000001", department="ENT")
        )
        self.assertEqual(create_resp.code, 200)
        doctor_id = create_resp.data.id

        # 查询医生
        get_resp = get_doctor_by_id_service(doctor_id)
        self.assertEqual(get_resp.code, 200)
        self.assertEqual(get_resp.data.name, "Dr. Liu")

        # 更新医生
        update_resp = update_doctor_service(
            doctor_id, UpdateDoctor(title="Chief", phone="13000000002")
        )
        self.assertEqual(update_resp.code, 200)
        self.assertEqual(update_resp.data.title, "Chief")

        # 列表查询
        list_resp = list_doctors_service()
        self.assertEqual(list_resp.code, 200)
        self.assertGreaterEqual(len(list_resp.data), 1)

        # 删除医生
        delete_resp = delete_doctor_service(doctor_id)
        self.assertEqual(delete_resp.code, 200)

        # 删除后查询应为 404
        missing_resp = get_doctor_by_id_service(doctor_id)
        self.assertEqual(missing_resp.code, 404)

    def test_patient_crud(self):
        # 先创建医生，满足外键约束
        doctor_resp = create_doctor_service(
            CreateDoctor(name="Dr. Zhang", phone="13000000003")
        )
        self.assertEqual(doctor_resp.code, 200)
        doctor_id = doctor_resp.data.id

        # 创建患者
        create_resp = create_patient_service(
            CreatePatient(
                name="Wang Mei",
                phone="13900000001",
                id_card="110101199001011234",
                primary_doctor_id=doctor_id,
            )
        )
        self.assertEqual(create_resp.code, 200)
        patient_id = create_resp.data.id

        # 查询患者
        get_resp = get_patient_by_id_service(patient_id)
        self.assertEqual(get_resp.code, 200)
        self.assertEqual(get_resp.data.name, "Wang Mei")

        # 更新患者
        update_resp = update_patient_service(
            patient_id, UpdatePatient(address="Beijing", phone="13900000002")
        )
        self.assertEqual(update_resp.code, 200)
        self.assertEqual(update_resp.data.address, "Beijing")

        # 列表查询
        list_resp = list_patients_service()
        self.assertEqual(list_resp.code, 200)
        self.assertGreaterEqual(len(list_resp.data), 1)

        # 删除患者
        delete_resp = delete_patient_service(patient_id)
        self.assertEqual(delete_resp.code, 200)

        # 删除后查询应为 404
        missing_resp = get_patient_by_id_service(patient_id)
        self.assertEqual(missing_resp.code, 404)


if __name__ == "__main__":
    unittest.main()
