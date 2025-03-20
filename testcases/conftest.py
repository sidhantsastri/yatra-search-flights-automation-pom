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

# ✅ Step 1: Add browser option for command-line argument
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests")
    parser.addoption("--url")

# ✅ Step 2: Fixture to get browser type from command-line argument
@pytest.fixture(scope="session", autouse=True)
def browser(request):
    return request.config.getoption("--browser")

# ✅ Step 3: Fixture to get url type from command-line argument like production or qa environment
@pytest.fixture(scope="session", autouse=True)
def url(request):
    return request.config.getoption("--url")

# ✅ Step 3: Setup fixture to launch browser based on the argument
@pytest.fixture(scope="class")
def setup(request, browser, url):
    if browser == "chrome":
        chrome_service = Service(ChromeDriverManager().install())
        # Driver - There has to be driver which drives through all the pages
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
    # Use a try-finally block to ensure the browser is always closed
    try:
        yield  # This is where the test case runs
    finally:
        driver.quit()

# Insert screenshots when test case is failed in the html report
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    extras = getattr(report, "extras", [])

    if report.when == "call":
        # Always add URL to report
        extras.append(pytest_html.extras.url("https://www.yatra.com/"))

        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Only add additional HTML on failure
            report_directory = os.path.dirname(item.config.option.htmlpath)
            file_name = report.nodeid.replace("::", "_").replace("/", "_") + ".png"  # Normalize file path
            destination_file = os.path.join(report_directory, file_name)

            # Ensure the report directory exists
            os.makedirs(report_directory, exist_ok=True)

            # Capture screenshot if the test fails
            driver = getattr(item.cls, "driver", None)  # Get the WebDriver instance from the test class
            if driver is not None and isinstance(driver, webdriver.Remote):
                try:
                    print(f"🖥️ Attempting to capture screenshot for failed test: {report.nodeid}")
                    print(f"📂 Destination file: {destination_file}")
                    driver.save_screenshot(destination_file)  # Save the screenshot
                    print(f"📸 Screenshot saved to: {destination_file}")

                    # Use a relative path for the HTML report
                    relative_file_path = os.path.relpath(destination_file, start=report_directory)
                    html = f'<div><img src="{relative_file_path}" alt="screenshot" style="width:300px; height:200px;" onclick="window.open(this.src)" align="right"/></div>'
                    extras.append(pytest_html.extras.html(html))
                    print(f"🖼️ Screenshot added to HTML report with relative path: {relative_file_path}")
                except Exception as e:
                    print(f"❌ Failed to capture or embed screenshot: {e}")
            else:
                print(f"❌ Driver instance not found or invalid: {driver}")

        report.extras = extras

def pytest_html_report_title(report):
    report.title = "My First Automation Test Case Report"