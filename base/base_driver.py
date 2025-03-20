import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# anything you are extending from the driver - and extending on top of webdriver methods - goes into the base driver

class BaseDriver:
    def __init__(self,driver, timeout =10):
        # Driver - There has to be driver which drives through all the pages -
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def page_scroll(self):
        # **Wait for flight results to load**
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//article[@ng-controller='scheduleController']")))
        # **SCROLL DOWN USING JAVASCRIPT EXECUTOR**
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Scroll to bottom
            time.sleep(2)  # Wait for new flights to load
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break  # Break if no new content is loaded
            last_height = new_height
        print("Reached the bottom of the flight results.")

    def wait_for_the_presence_of_all_elements(self, locator_type, locator):
        list_of_elements = self.wait.until(
            EC.presence_of_all_elements_located(
                (locator_type, locator)))
        return list_of_elements

    def wait_until_element_is_clickable(self, locator_type, locator):
        element = self.wait.until(EC.element_to_be_clickable((locator_type, locator)))
        return element

    def wait_until_visibility_of_the_element(self, locator_type, locator):
        visible_element = self.wait.until(EC.visibility_of_element_located((locator_type, locator)))
        return visible_element

    def wait_until_invisibility_of_the_element(self, locator_type, locator):
        invisible_element = self.wait.until(EC.invisibility_of_element_located((locator_type, locator)))
        return invisible_element

    def click_when_clickable(self, element):
        self.wait.until(EC.element_to_be_clickable(element)).click()


