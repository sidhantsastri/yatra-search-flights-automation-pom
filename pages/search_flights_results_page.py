import logging
import time
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from utilities.utils import Utils

class SearchFlightResults(BaseDriver):
    # use the custom logger at the class level
    log = Utils.custum_logger(logLevel=logging.WARNING)
    def __init__(self, driver):
        super().__init__(driver)
        #self.driver = driver
        #self.wait = wait

    # Locators
    # ONE_STOP_FLIGHTS = "//p[@class='font-lightgrey bold'][normalize-space()='1']"
    # TWO_STOP_FLIGHTS = "//p[@class='font-lightgrey bold'][normalize-space()='2']"
    # NON_STOP_FLIGHTS = "//p[@class='font-lightgrey bold'][normalize-space()='0']"

    # Locators (Generic for Any Stop Count)
    FLIGHT_STOP_XPATH = "//p[@class='font-lightgrey bold'][normalize-space()='{}']"

    #SEARCH_FLIGHTS_RESULTS = "//span[contains(@class, 'dotted-borderbtm') and contains(text(), '1 Stop')]"
    # Dynamic XPath using format placeholders
    SEARCH_FLIGHTS_RESULTS = "//span[contains(@class, 'dotted-borderbtm') and contains(text(), '{}')]"

    def get_flight_stop_element(self, stop_count):
        """ Dynamically find the stop filter button """
        xpath = self.FLIGHT_STOP_XPATH.format(stop_count.split()[0])  # Extract number from '1 Stop' → '1'
        return self.wait_until_element_is_clickable(By.XPATH, xpath)

    def get_search_flights_results(self, stop_count):
        """ Dynamically fetch all flight results based on stops """
        xpath = self.SEARCH_FLIGHTS_RESULTS.format(stop_count)
        return self.wait_for_the_presence_of_all_elements(By.XPATH, xpath)

    def filter_flights_by_stops(self, stop_count):
        """ Clicks the flight stop filter dynamically """
        try:
            self.get_flight_stop_element(stop_count).click()
            self.log.warning(f"Selected flights with {stop_count}")
            time.sleep(2)
        except Exception as e:
            self.log.error(f"Failed to select stop filter: {stop_count}. Error: {e}")

    # def filter_flights_by_stops(self, by_stop):
    #     if by_stop == "1 Stop":
    #         self.get_one_stop_flights().click()
    #         # the log is in class level - so inorder to access it
    #         self.log.warning("Selected flights with 1 stop")
    #         time.sleep(2)
    #     elif by_stop == "2 Stops":
    #         self.get_two_stop_flights().click()
    #         self.log.warning("Selected flights with 2 stop")
    #         time.sleep(2)
    #     elif by_stop == "Non Stop":
    #         self.get_non_stop_flights().click()
    #         self.log.warning("Selected flights with non stop")
    #         time.sleep(2)
    #     else:
    #         self.log.warning("Please provide valid option")