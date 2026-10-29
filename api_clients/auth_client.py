# -*- coding: utf-8 -*-
"""
@File    : auth_client.py
@Time    : 2026/10/29 13:07
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
from .base_client import BaseClient


class AuthClient(BaseClient):

    def login(self, username: str, password: str) -> str:
        body = self.post("/api/auth/login", json={
            "username": username, "password": password
        })
        token = body["data"]["token"]
        self.set_token(token)
        return token

    def get_me(self) -> dict:
        return self.get("/api/auth/me")["data"]