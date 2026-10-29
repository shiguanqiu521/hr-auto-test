# -*- coding: utf-8 -*-
"""
@File    : test_login_parametrize.py
@Time    : 2026/10/29 15:48
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
# -*- coding: utf-8 -*-
import pytest
from playwright.sync_api import Page


@pytest.mark.smoke
class TestLoginParametrize:
    """数据驱动登录测试 - 一组逻辑，多组数据"""

    @pytest.mark.parametrize("username, password, expect_success", [
        ("admin", "admin123", True),          # 正确账号
        ("admin", "wrong", False),            # 错误密码
        ("admin", "", False),                 # 空密码
        ("", "admin123", False),              # 空用户名
        ("nonexist", "admin123", False),      # 不存在用户
    ])
    def test_login_cases(self, login_page, username, password, expect_success):
        login_page.login(username, password)
        if expect_success:
            login_page.expect_success()
        else:
            login_page.expect_failed()