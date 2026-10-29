# -*- coding: utf-8 -*-
"""
@File    : test_login.py
@Time    : 2026/10/27 11:21
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import pytest

@pytest.mark.smoke
class TestLogin:
    """登录功能测试  -  冒烟测试"""

    def test_login_success(self,login_page):
        """登录成功"""
        login_page.login('admin','admin123')
        login_page.expect_success()

    def test_login_wrong_password(self,login_page):
        """登录失败"""
        login_page.login('admin','234324')
        login_page.expect_failed()