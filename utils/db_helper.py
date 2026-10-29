# -*- coding: utf-8 -*-
"""
@File    : db_helper.py
@Time    : 2026/10/29 15:30
@Author  : Your Name
@Version : 1.0
@Desc    : 数据库验证工具 - 验证 API 操作后的数据一致性
"""
import pymysql
from utils.config import Config
from utils.logger import get_logger

logger = get_logger("DBHelper")


class DBHelper:

    def __init__(self):
        self.conn = pymysql.connect(**Config.DB_CONFIG)
        self.conn.autocommit(True)

    def _cursor(self, dictionary=True):
        return self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def query(self, sql: str, params: tuple = None) -> list:
        with self._cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def execute(self, sql: str, params: tuple = None) -> int:
        with self._cursor() as cur:
            cur.execute(sql, params)
            self.conn.commit()
            return cur.rowcount

    # ---- 员工表验证 ----

    def get_employee_by_id(self, emp_id: int) -> dict | None:
        rows = self.query(
            "SELECT * FROM employee WHERE id = %s AND deleted = 0",
            (emp_id,)
        )
        return rows[0] if rows else None

    def get_employee_by_phone(self, phone: str) -> dict | None:
        rows = self.query(
            "SELECT * FROM employee WHERE phone = %s AND deleted = 0",
            (phone,)
        )
        return rows[0] if rows else None

    def is_soft_deleted(self, emp_id: int) -> bool:
        rows = self.query(
            "SELECT deleted FROM employee WHERE id = %s",
            (emp_id,)
        )
        return rows[0]["deleted"] == 1 if rows else False

    def count_employees(self, name: str = None, department: str = None) -> int:
        sql = "SELECT COUNT(*) as cnt FROM employee WHERE deleted = 0"
        params = []
        if name:
            sql += " AND name LIKE %s"
            params.append(f"%{name}%")
        if department:
            sql += " AND department LIKE %s"
            params.append(f"%{department}%")
        return self.query(sql, tuple(params))[0]["cnt"]

    # ---- 部门表验证 ----

    def get_department_by_id(self, dept_id: int) -> dict | None:
        rows = self.query(
            "SELECT * FROM department WHERE id = %s AND deleted = 0",
            (dept_id,)
        )
        return rows[0] if rows else None

    def is_dept_soft_deleted(self, dept_id: int) -> bool:
        rows = self.query(
            "SELECT deleted FROM department WHERE id = %s",
            (dept_id,)
        )
        return rows[0]["deleted"] == 1 if rows else False

    def close(self):
        self.conn.close()
