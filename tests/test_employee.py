# -*- coding: utf-8 -*-
"""
@File    : test_employee.py
@Time    : 2026/10/29 13:57
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import pytest
from api_clients.employee_client import EmployeeClient
from builders.employee_builder import EmployeeBuilder, valid_employee, invalid_missing_name, invalid_bad_phone, invalid_bad_status


@pytest.mark.smoke
class TestEmployeeCreate:

    def test_create(self, employee_client: EmployeeClient):
        emp = employee_client.create_random(**valid_employee(name="张三", department="研发部"))
        assert emp["name"] == "张三"
        assert emp["id"] is not None

    def test_create_builder(self, employee_client: EmployeeClient):
        data = EmployeeBuilder().with_name("李四").with_department("人事部").with_past_date(60).build()
        emp = employee_client.create_random(**data)
        assert emp["name"] == "李四"


@pytest.mark.smoke
class TestEmployeeQuery:

    def test_get_detail(self, employee_client: EmployeeClient, fresh_employee):
        detail = employee_client.get(fresh_employee["id"])
        assert detail["id"] == fresh_employee["id"]

    def test_search_by_name(self, employee_client: EmployeeClient, fresh_employee):
        result = employee_client.list(name=fresh_employee["name"][:2])
        assert result["total"] >= 1

    def test_search_no_result(self, employee_client: EmployeeClient):
        result = employee_client.list(name="不存在99999")
        assert result["total"] == 0


@pytest.mark.regression
class TestEmployeeValidation:

    def test_empty_name(self, employee_client: EmployeeClient):
        resp = employee_client.raw("POST", "/api/employees", json=invalid_missing_name())
        assert resp.status_code == 400

    def test_bad_phone(self, employee_client: EmployeeClient):
        resp = employee_client.raw("POST", "/api/employees", json=invalid_bad_phone())
        assert resp.status_code == 400

    def test_bad_status(self, employee_client: EmployeeClient):
        resp = employee_client.raw("POST", "/api/employees", json=invalid_bad_status())
        assert resp.status_code == 400

    def test_duplicate_phone(self, employee_client: EmployeeClient, fresh_employee):
        resp = employee_client.raw("POST", "/api/employees", json=valid_employee(phone=fresh_employee["phone"]))
        assert resp.status_code == 409


@pytest.mark.regression
class TestEmployeeUpdate:

    def test_update(self, employee_client: EmployeeClient, fresh_employee):
        updated = employee_client.update(
            fresh_employee["id"],
            name=fresh_employee["name"], phone=fresh_employee["phone"],
            department="测试部", position="高级",
            hireDate=fresh_employee["hireDate"], status="试用期"
        )
        assert updated["department"] == "测试部"
        assert updated["status"] == "试用期"

    def test_update_nonexistent(self, employee_client: EmployeeClient):
        resp = employee_client.raw("PUT", "/api/employees/99999", json=valid_employee())
        assert resp.status_code == 404


@pytest.mark.regression
class TestEmployeeDelete:

    def test_delete(self, employee_client: EmployeeClient):
        emp = employee_client.create_random(**valid_employee())
        employee_client.delete(emp["id"])
        resp = employee_client.raw("GET", f"/api/employees/{emp['id']}")
        assert resp.status_code == 404

    def test_delete_twice(self, employee_client: EmployeeClient):
        emp = employee_client.create_random(**valid_employee())
        employee_client.delete(emp["id"])
        resp = employee_client.raw("DELETE", f"/api/employees/{emp['id']}")
        assert resp.status_code == 404


@pytest.mark.regression
class TestFixtureIsolation:

    def test_isolation(self, fresh_employee, fresh_employee_named):
        e1 = fresh_employee
        e2 = fresh_employee_named("隔离测试")
        assert e1["id"] != e2["id"]

    def test_batch(self, batch_employees):
        emps = batch_employees(count=5)
        assert len(emps) == 5
        assert len(set(e["id"] for e in emps)) == 5