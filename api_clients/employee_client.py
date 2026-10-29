# -*- coding: utf-8 -*-
"""
@File    : employee_client.py
@Time    : 2026/10/29 13:30
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import random
from .base_client import BaseClient


class EmployeeClient(BaseClient):

    def create(self, **fields) -> dict:
        return self.post("/api/employees", json=fields)["data"]

    def create_random(self, **fields) -> dict:
        if "phone" not in fields:
            fields["phone"] = f"138{random.randint(10000000, 99999999)}"
        body = self.post("/api/employees", json=fields)
        if body.get("code") == 409:
            fields["phone"] = f"139{random.randint(10000000, 99999999)}"
            body = self.post("/api/employees", json=fields)
        if body.get("code") != 200:
            raise AssertionError(f"create_random 失败: {body.get('message')}")
        return body["data"]

    def get(self, emp_id:int) -> dict:
        return super().get(f"/api/employees/{emp_id}")["data"]

    def list(self, name: str = None, department: str = None,
             page: int = 1, size: int = 10) -> dict:
        params = {"page": page, "size": size}
        if name: params["name"] = name
        if department: params["department"] = department
        return super().get("/api/employees", params=params)["data"]

    def update(self, emp_id: int, **fields) -> dict:
        return super().put(f"/api/employees/{emp_id}", json=fields)["data"]

    def delete(self, emp_id: int):
        return super().delete(f"/api/employees/{emp_id}")