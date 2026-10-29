# -*- coding: utf-8 -*-
"""
@File    : conftest.py
@Time    : 2026/10/27 13:19
@Author  : Your Name
@Version : 1.0
@Desc    : 
"""
import time
import pytest
from playwright.sync_api import Page, BrowserContext
from api_clients.auth_client import AuthClient
from pages.login_page import LoginPage
from utils.logger import get_logger
from utils.config import Config
from utils.db_helper import DBHelper
from utils.report_notifier import ReportNotifier
from api_clients.employee_client import EmployeeClient
from api_clients.department_client import DepartmentClient
from builders.employee_builder import EmployeeBuilder, valid_employee

logger = get_logger("conftest")
Config.validate()

_session_start = time.time()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "locale": "zh-CN",
        "ignore_https_errors": True,
    }


@pytest.fixture
def page(context: BrowserContext):
    p = context.new_page()
    yield p
    p.close()


@pytest.fixture(scope="session")
def auth_client() -> AuthClient:
    client = AuthClient()
    client.login(Config.LOGIN_USERNAME, Config.LOGIN_PASSWORD)
    return client


@pytest.fixture
def login_page(page: Page):
    lp = LoginPage(page)
    lp.open()
    return lp


@pytest.fixture
def logged_in_page(page: Page):
    lp = LoginPage(page)
    lp.open()
    lp.login()
    lp.expect_success()
    return page


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logstart(nodeid, location):
    logger.info(f"▶ {nodeid}")


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_logfinish(nodeid, location):
    logger.info(f"✅ {nodeid}")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page") or item.funcargs.get("logged_in_page")
        if page:
            page.screenshot(path=f"screenshots/FAIL_{item.name}.png")
            logger.error(f"❌ {item.name}")


@pytest.fixture(scope="session")
def employee_client(auth_client: AuthClient) -> EmployeeClient:
    c = EmployeeClient()
    c.set_token(auth_client._token)
    return c


@pytest.fixture(scope="session")
def department_client(auth_client: AuthClient) -> DepartmentClient:
    c = DepartmentClient()
    c.set_token(auth_client._token)
    return c


@pytest.fixture
def fresh_employee(employee_client: EmployeeClient):
    emp = employee_client.create_random(**valid_employee())
    yield emp
    try: employee_client.delete(emp["id"])
    except: pass


@pytest.fixture
def fresh_employee_named(employee_client: EmployeeClient):
    def _create(name: str, **kw):
        return employee_client.create_random(**valid_employee(name=name, **kw))
    yield _create


@pytest.fixture
def batch_employees(employee_client: EmployeeClient):
    def _create(count: int = 3, **kw):
        return [employee_client.create_random(**valid_employee(**kw)) for _ in range(count)]
    yield _create


@pytest.fixture
def fresh_department(department_client: DepartmentClient):
    import random
    dept = department_client.create(name=f"测试部门{random.randint(1000,9999)}")
    yield dept
    try: department_client.delete(dept["id"])
    except: pass


@pytest.fixture(scope="session")
def db() -> DBHelper:
    helper = DBHelper()
    yield helper
    helper.close()


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    duration = time.time() - _session_start
    summary = session.config.pluginmanager.get_plugin("terminalreporter")
    if not summary:
        return

    stats = summary.stats
    passed = len(stats.get("passed", []))
    failed = len(stats.get("failed", []))
    error = len(stats.get("error", []))
    skipped = len(stats.get("skipped", []))

    notifier = ReportNotifier(Config.WEBHOOK_URL)
    msg = notifier.format_summary(passed, failed, error, skipped, duration)
    notifier.send_wechat("HR系统自动化测试", msg)
    logger.info(f"测试完成: {passed} passed, {failed} failed, {error} error, {skipped} skipped, {duration:.1f}s")