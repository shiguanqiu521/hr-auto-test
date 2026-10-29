# -*- coding: utf-8 -*-
"""
@File    : loginpage.py
@Time    : 2026/10/27 9:14
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
from pages.base_page import BasePage
from playwright.sync_api import expect,Page
from utils.logger import get_logger

logger = get_logger('LoginPage')


class LoginPage(BasePage):

    URL = 'http://106.12.144.134/'
    #定位器
    USERNAME_INPUT = None
    PASSWORD_INPUT = None
    LOGIN_BUTTON = None
    SUCCESS_MESSAGE = None
    ERROR_MESSAGE = None

    def __init__(self,page):
        super().__init__(page)
        # 初始化定位器
        self.USERNAME_INPUT = page.get_by_placeholder("请输入用户名")
        self.PASSWORD_INPUT = page.get_by_placeholder("请输入密码")
        self.LOGIN_BUTTON = page.get_by_role('button',name='登 录')
        self.SUCCESS_MESSAGE = page.get_by_text('登录成功，欢迎 系统管理员')
        self.ERROR_MESSAGE = page.get_by_text('用户名或密码错误')

    def open(self):
        self.goto(self.URL)

    def login(self,username,password):
        """登录流程"""
        logger.info(f"登录操作: username={username}")
        self.USERNAME_INPUT.fill(username)
        self.PASSWORD_INPUT.fill(password)
        self.LOGIN_BUTTON.click()
        logger.info("点击登录按钮")

    def expect_success(self,success_message='登录成功，欢迎 系统管理员'):
        """验证登录成功"""
        expect(self.SUCCESS_MESSAGE).to_be_visible()
        expect(self.SUCCESS_MESSAGE).to_have_text(success_message)
        logger.info("登录成功 ✓")

    def expect_failed(self,error_text='用户名或密码错误'):
        """验证登录失败"""
        expect(self.ERROR_MESSAGE).to_be_visible()

    def expect_empty_form_error(self):
        """验证空表单错误"""
        logger.info("验证空表单错误")
        expect(self.page.get_by_text("用户名和密码不能为空")).to_be_visible()