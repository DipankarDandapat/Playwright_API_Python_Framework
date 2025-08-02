import os
import sys
from datetime import datetime
from pathlib import Path

import pytest
from dotenv import load_dotenv

from playwright.sync_api import APIRequestContext, Playwright
from typing import Generator
import logging

from API_Utilities import logger_utility

log = logger_utility.customLogger()


class Environment:
    def __init__(self, env_name=None):
        self.env_name = env_name or os.environ.get("ENVIRONMENT", "staging")

        # Use current working directory as project root
        self.project_root = Path.cwd()
        self.env_file = self.project_root / f".env.{self.env_name}"

        print(f"Looking for env file at: {self.env_file}")  # Debug line

        if not self.env_file.exists():
            print(f"Error: Environment file {self.env_file} not found.")
            print(f"Available environments: {self._get_available_environments()}")
            sys.exit(1)

        load_dotenv(dotenv_path=self.env_file, override=True)
        print(f"Loaded environment configuration from {self.env_file}")

    def _get_available_environments(self):
        return [f.name.replace(".env.", "") for f in self.project_root.glob(".env.*")]

def pytest_addoption(parser):
    parser.addoption("--env", action="store", default="staging", help="Environment to run tests against")


@pytest.fixture(scope="session", autouse=True)
def setup_environment(request):
    env_name = request.config.getoption("--env")
    log.info(f"Setting up environment: {env_name}")

    # Load environment using Environment class
    Environment(env_name)

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright, ) -> Generator[APIRequestContext, None, None]:
    """
    Method to create the API request context
    :param playwright:
    :return:
    """
    request_context = playwright.request.new_context()
    log.info("testcase start now .....")

    yield request_context
    request_context.dispose()
    log.info("testcase End now .....")



def _create_report_path():
    current_directory = os.getcwd()
    new_folder_path = os.path.join(current_directory, 'execution_reports')
    if not os.path.exists(new_folder_path):
        os.mkdir(new_folder_path)
    return new_folder_path



@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    extra = getattr(report, 'extras', [])

    if report.when == 'call' or report.when == 'setup':
        xfail = hasattr(report, 'wasxfail')
        if report.failed and not xfail:
            # Use caplog to capture logs
            caplog = item.funcargs.get('caplog')
            if caplog:
                log_text = '\n'.join([record.getMessage() for record in caplog.get_records('setup') + caplog.get_records('call')])
                extra.append(pytest_html.extras.text(log_text, 'Logs'))

        report.extras = extra


# Configure the HTML report path and name
def pytest_configure(config):
    config.option.htmlpath = os.path.join(_create_report_path(), 'Test_Automation_Report_' + datetime.now().strftime(
        "%d-%m-%Y %H-%M-%S") + ".html")


# Setup the logging configuration
@pytest.fixture(scope='session', autouse=True)
def configure_logging():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    yield

    logger.removeHandler(console_handler)


# Ensure caplog is available as a fixture
@pytest.fixture(autouse=True)
def setup_caplog(caplog):
    yield caplog
