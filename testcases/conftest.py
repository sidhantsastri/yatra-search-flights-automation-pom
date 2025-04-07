import os
import pytest
import pytest_html
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# 1. Define a default reports directory at the module level
DEFAULT_REPORT_DIR = os.path.join(os.getcwd(), "reports")
SCREENSHOTS_DIR = os.path.join(DEFAULT_REPORT_DIR, "screenshots")


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests")
    parser.addoption("--url", action="store", default="https://www.yatra.com")
    #parser.addoption("--html", action="store", default=os.path.join(DEFAULT_REPORT_DIR, "report.html"),
    #                 help="Path to html report")


@pytest.fixture(scope="session", autouse=True)
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session", autouse=True)
def url(request):
    return request.config.getoption("--url")


# 2. Create a session-scoped fixture to ensure report directories exist
@pytest.fixture(scope="session", autouse=True)
def setup_report_dirs():
    os.makedirs(DEFAULT_REPORT_DIR, exist_ok=True)
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    yield


@pytest.fixture(scope="class")
def setup(request, browser, url):
    if browser == "chrome":
        chrome_service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=chrome_service)
    elif browser == "firefox":
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service)
    elif browser == "edge":
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.get(url)
    driver.maximize_window()
    request.cls.driver = driver

    yield
    driver.quit()


# 3. Simplified and robust report generation
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call":
        extras.append(pytest_html.extras.url(item.funcargs["url"]))

        if report.failed:
            try:
                driver = item.cls.driver
                screenshot_name = f"{item.nodeid.replace('::', '_')}.png"
                screenshot_path = os.path.join(SCREENSHOTS_DIR, screenshot_name)
                driver.save_screenshot(screenshot_path)

                # Use relative path for HTML report
                rel_path = os.path.relpath(screenshot_path, start=DEFAULT_REPORT_DIR)
                extras.append(pytest_html.extras.image(rel_path))
            except Exception as e:
                print(f"⚠️ Could not capture screenshot: {e}")

        report.extras = extras


def pytest_html_report_title(report):
    report.title = "Yatra.com Test Automation Report"