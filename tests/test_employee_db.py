# -*- coding: utf-8 -*-
"""
@File    : test_employee_db.py
@Time    : 2026/10/29 15:21
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import random

# -*- coding: utf-8 -*-
import pytest
from builders.employee_builder import valid_employee


@pytest.mark.regression
class TestEmployeeDB:
    """数据库层验证 - 确认 API 操作后数据真的写对了"""

    def test_create_writes_to_db(self, employee_client, db):
        emp = employee_client.create_random(**valid_employee())
        try:
            row = db.get_employee_by_id(emp["id"])
            assert row is not None, "DB 中查不到刚创建的员工"
            assert row["name"] == emp["name"]
            assert row["phone"] == emp["phone"]
            assert row["department"] == emp["department"]
            assert row["status"] == emp["status"]
        finally:
            employee_client.delete(emp["id"])

    def test_delete_is_soft_delete(self, employee_client, db):
        emp = employee_client.create_random(**valid_employee())
        employee_client.delete(emp["id"])

        # API 查不到
        resp = employee_client.raw("GET", f"/api/employees/{emp['id']}")
        assert resp.status_code == 404

        # DB 里还在，但 deleted=1
        assert db.is_soft_deleted(emp["id"]), "软删除标记未置为1"

    def test_update_reflects_in_db(self, employee_client, db):
        emp = employee_client.create_random(**valid_employee())
        try:
            employee_client.update(emp["id"], **valid_employee(name="DB验证改名", position="DB验证岗位"))
            row = db.get_employee_by_id(emp["id"])
            assert row["name"] == "DB验证改名"
            assert row["position"] == "DB验证岗位"
        finally:
            employee_client.delete(emp["id"])

    def test_count_matches_api(self, employee_client, db):
        unique_name = f"计数测试{random.randint(10000, 99999)}"
        before = db.count_employees(name=unique_name)
        emp = employee_client.create_random(**valid_employee(name=unique_name))
        try:
            assert db.count_employees(name=unique_name) == before + 1
        finally:
            employee_client.delete(emp["id"])
            assert db.count_employees(name=unique_name) == before