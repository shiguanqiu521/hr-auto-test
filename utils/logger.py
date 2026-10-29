# -*- coding: utf-8 -*-
"""
@File    : logger.py
@Time    : 2026/10/27 16:54
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import logging
import os
from datetime import datetime


def get_logger(name: str) -> logging.Logger:
    """获取日志记录器"""
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # 日志目录
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # 日志文件（按日期）
    today = datetime.now().strftime("%Y-%m-%d")
    file_handler = logging.FileHandler(
        f"{log_dir}/test_{today}.log",
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)

    # 控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 格式
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)-8s %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
