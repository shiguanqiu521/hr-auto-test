# -*- coding: utf-8 -*-
"""
@File    : data_factory.py
@Time    : 2026/10/28 16:09
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import requests
import pymysql
import random
from typing import Dict,Any

class DataFactory:
    """测试数据工厂：创建 → 使用 → 清理"""
    def __init__(self,base_url:str,db_config:dict):
        self.base_url = base_url
        self.db_config = db_config
        self._created_records = []

    def create_employee(self, name: str = None, dept: str = "技术部",
                        phone: str = None, **kwargs) -> Dict[str, Any]:
        """通过 API 创建员工"""
        




