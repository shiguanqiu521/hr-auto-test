# -*- coding: utf-8 -*-
"""
@File    : employee_builder.py
@Time    : 2026/10/29 13:37
@Author  : Your Name
@Version : 1.0
@Desc    :
"""
import random
from datetime import datetime, timedelta


class EmployeeBuilder:

    def __init__(self):
        suffix = random.randint(1000, 9999)
        self._data = {
            "name": f"测试员工{suffix}",
            "phone": f"138{random.randint(10000000, 99999999)}",
            "department": "研发部",
            "position": "测试工程师",
            "hireDate": "2026-01-01",
            "status": "在职",
        }

    def with_name(self, name: str):
        self._data["name"] = name
        return self

    def with_phone(self, phone: str):
        self._data["phone"] = phone
        return self

    def with_department(self, d: str):
        self._data["department"] = d
        return self

    def with_position(self, p: str):
        self._data["position"] = p
        return self

    def with_hire_date(self, d: str):
        self._data["hireDate"] = d
        return self

    def with_status(self, s: str):
        self._data["status"] = s
        return self

    def with_past_date(self, days: int = 30):
        d = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        self._data["hireDate"] = d
        return self

    def build(self) -> dict:
        return self._data.copy()


def valid_employee(**overrides) -> dict:
    b = EmployeeBuilder()
    for k, v in overrides.items():
        getattr(b, f"with_{k}")(v)
    return b.build()


def invalid_missing_name() -> dict:
    d = EmployeeBuilder().build()
    d["name"] = ""
    return d


def invalid_bad_phone() -> dict:
    d = EmployeeBuilder().build()
    d["phone"] = "123"
    return d


def invalid_bad_status() -> dict:
    d = EmployeeBuilder().build()
    d["status"] = "未知"
    return d
