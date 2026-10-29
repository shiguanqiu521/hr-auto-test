# -*- coding: utf-8 -*-
"""
@File    : department_client.py
@Time    : 2026/10/29 13:36
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import random
from .base_client import BaseClient


class DepartmentClient(BaseClient):

    def create(self, **fields) -> dict:
        body = self.post("/api/departments", json=fields)
        if body.get("code") == 409:
            fields["name"] = f"测试部门{random.randint(1000, 9999)}"
            body = self.post("/api/departments", json=fields)
        return body["data"]

    def list(self, name: str = None) -> list:
        params = {"name": name} if name else {}
        return self.get("/api/departments", params=params)["data"]

    def delete(self, dept_id: int):
        return super().delete(f"/api/departments/{dept_id}")