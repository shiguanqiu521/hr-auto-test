# -*- coding: utf-8 -*-
"""
@File    : base_page.py
@Time    : 2026/10/26 21:35
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
from playwright.async_api import Page,expect
from playwright.sync_api import Locator

from utils.logger import get_logger

logger = get_logger('BasePage')


class BasePage:
    def __init__(self,page:Page):
        self.page = page

    def goto(self,url:str,wait_until = 'networkidle'):
        """打开网页"""
        logger.info(f'打开页面：{url}')
        self.page.goto(url,wait_until=wait_until)

    def click(self,locator: Locator):
        """点击元素"""
        logger.info(f'点击元素')
        locator.click()

    def fill(self,locator: Locator,text:str):
        """输入文本"""
        logger.info(f'输入文本: {text}')
        locator.fill(text)

    def get_text(self,locator:Locator):
        """获取文本"""
        logger.info(f'获取文本')
        return locator.text_content() or ''

    def is_visible(self,locator:str) -> bool:
        """判断元素是否可见"""
        try:
            expect(locator).to_be_visible()
            return True
        except:
            return False

    def wait_for_element(self,locator:Locator,timeout:int=5000):
        """等待元素出现"""
        locator.wait_for(state='visible',timeout=timeout)

    def screenshot(self,name):
        """截图"""
        path = f'screenshots/{name}.png'
        self.page.screenshot(path=path)
        logger.info(f"截图: {path}")

    def expect_visible(self, locator: Locator):
        expect(locator).to_be_visible()

    def expect_text(self, locator: Locator, text: str):
        expect(locator).to_have_text(text)

    def expect_url_contains(self, text: str):
        expect(self.page).to_have_url(f".*{text}.*")




