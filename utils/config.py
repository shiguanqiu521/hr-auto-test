# -*- coding: utf-8 -*-
"""
@File    : config.py
@Time    : 2026/10/29 10:21
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import os
from dotenv import load_dotenv

load_dotenv()

def _getenv(key: str, default: str = "") -> str:
    return os.getenv(key, default).strip()


class Config:
    API_BASE_URL = _getenv('API_BASE_URL')
    FRONTEND_URL = _getenv('FRONTEND_URL')

    DB_CONFIG = {
        'host': _getenv("DB_HOST"),
        'port': int(_getenv("DB_PORT")),
        'user': _getenv("DB_USER"),
        'password': _getenv("DB_PASSWORD"),
        'database': _getenv("DB_NAME"),
        'charset': 'utf8mb4',
    }

    LOGIN_USERNAME = _getenv('LOGIN_USERNAME', 'admin')
    LOGIN_PASSWORD = _getenv('LOGIN_PASSWORD', 'admin123')
    WEBHOOK_URL = _getenv('WEBHOOK_URL')

    @classmethod
    def validate(cls):
        missing = []
        if not cls.DB_CONFIG["password"]:
            missing.append("DB_PASSWORD")
        if not cls.LOGIN_PASSWORD:
            missing.append("LOGIN_PASSWORD")
        if missing:
            raise RuntimeError(
                f"缺少必要配置: {', '.join(missing)}\n"
                f"请在 .env 文件中设置"
            )