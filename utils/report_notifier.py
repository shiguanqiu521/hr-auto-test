# -*- coding: utf-8 -*-
"""
@File    : report_notifier.py
@Time    : 2026/10/29 15:30
@Author  : Your Name
@Version : 1.0
@Desc    : 测试报告推送 - 企业微信/钉钉 webhook
"""
import requests
from utils.logger import get_logger

logger = get_logger("ReportNotifier")


class ReportNotifier:

    def __init__(self, webhook_url: str = ""):
        self.webhook_url = webhook_url

    def send_wechat(self, title: str, content: str):
        """企业微信机器人 webhook"""
        if not self.webhook_url:
            logger.warning("WEBHOOK_URL 未配置，跳过推送")
            return
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "content": f"## {title}\n{content}"
            }
        }
        try:
            resp = requests.post(self.webhook_url, json=payload, timeout=10)
            logger.info(f"企业微信推送: {resp.status_code} {resp.text}")
        except Exception as e:
            logger.error(f"企业微信推送失败: {e}")

    def send_dingtalk(self, title: str, content: str):
        """钉钉机器人 webhook"""
        if not self.webhook_url:
            logger.warning("WEBHOOK_URL 未配置，跳过推送")
            return
        payload = {
            "msgtype": "markdown",
            "markdown": {
                "title": title,
                "text": f"## {title}\n{content}"
            }
        }
        try:
            resp = requests.post(self.webhook_url, json=payload, timeout=10)
            logger.info(f"钉钉推送: {resp.status_code} {resp.text}")
        except Exception as e:
            logger.error(f"钉钉推送失败: {e}")

    def format_summary(self, passed: int, failed: int, error: int, skipped: int, duration: float) -> str:
        total = passed + failed + error + skipped
        status_emoji = "✅" if failed == 0 and error == 0 else "❌"
        return (
            f"{status_emoji} **测试完成**\n\n"
            f"- 总计: {total}\n"
            f"- 通过: {passed}\n"
            f"- 失败: {failed}\n"
            f"- 错误: {error}\n"
            f"- 跳过: {skipped}\n"
            f"- 耗时: {duration:.1f}s"
        )
