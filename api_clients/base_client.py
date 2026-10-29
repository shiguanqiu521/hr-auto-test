# -*- coding: utf-8 -*-
"""
@File    : base_client.py
@Time    : 2026/10/29 10:44
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from utils.logger import get_logger
from utils.config import Config

logger = get_logger("APIClient")


class BaseClient:

    def __init__(self, base_url: str = None, token: str = None):
        self.base_url = base_url or Config.API_BASE_URL
        self._token = token
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
            allowed_methods=["GET", "POST", "PUT", "DELETE"],
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        session.headers.update({"Content-Type": "application/json;charset=UTF-8"})
        return session

    def set_token(self, token: str):
        self._token = token
        self.session.headers["Authorization"] = f"Bearer {token}"

    def _log(self, method: str, url: str, **kwargs):
        logger.debug(f"→ {method} {url}")

    def _check(self, resp: requests.Response, expected_code: int = 200) -> dict:
        body = resp.json()
        if body.get("code") != expected_code:
            raise AssertionError(f"API 异常: code={body.get('code')}, msg={body.get('message')}")
        return body

    def get(self, path: str, params: dict = None, expected_code: int = 200) -> dict:
        url = f"{self.base_url}{path}"
        self._log("GET", url)
        resp = self.session.get(url, params=params)
        logger.debug(f"← {resp.status_code}")
        return self._check(resp, expected_code)

    def post(self, path: str, json: dict = None, expected_code: int = 200) -> dict:
        url = f"{self.base_url}{path}"
        self._log("POST", url)
        resp = self.session.post(url, json=json)
        logger.debug(f"← {resp.status_code}")
        return self._check(resp, expected_code)

    def put(self, path: str, json: dict = None, expected_code: int = 200) -> dict:
        url = f"{self.base_url}{path}"
        self._log("PUT", url)
        resp = self.session.put(url, json=json)
        return self._check(resp, expected_code)

    def delete(self, path: str, expected_code: int = 200) -> dict:
        url = f"{self.base_url}{path}"
        self._log("DELETE", url)
        resp = self.session.delete(url)
        return self._check(resp, expected_code)

    def raw(self, method: str, path: str, **kwargs) -> requests.Response:
        """原始响应（用于断言 400/404/409）"""
        url = f"{self.base_url}{path}"
        self._log(method.upper(), url)
        return self.session.request(method, url, **kwargs)