import time
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
import pytest
import softest
from selenium.webdriver.support.wait import WebDriverWait

from pages.yatra_launch_page import LaunchPage
from utilities.utils import Utils
from ddt import ddt, data, file_data, unpack



@pytest.mark.usefixtures("setup")
@ddt
class TestSearchAndVerifyFilter(softest.TestCase):
    # use the custom logger at the class level
    log = Utils.custum_logger()

    # This class setup will be automatically called first before all the test methods in the page class
    @pytest.fixture(autouse=True)
    # Create a new method where all objects for the pages and utils
    def class_setup(self):
        # 2)Provide going from location
        self.lp = LaunchPage(self.driver)  # Creates an object of LaunchPage and passes driver
        self.ut = Utils()

    def setup_method(self, method):
        """ Ensures a fresh page load for every test case """
        self.driver.get("https://www.yatra.com")  # Replace with the actual URL
        time.sleep(2)  # Allow the page to load

    #data driven testing -- use decorator - data and unpack
    # @data(("New Delhi", "New", "28 March 2025", "2 Stops"))
    # @unpack

    # Data-driven testing from json data
    #@file_data("../testdata/testdata.json")

    # Data-driven testing from yaml data
    #@needs_yaml
    #@file_data("../testdata/testyml.yaml")

    # Data-Driven testing from excel
    # @data(*Utils.read_data_from_excel("C:\\python-selenium\\TestFrameworkDemo\\testdata\\test_data_excel.xlsx", "Sheet1"))
    # @unpack

    # Data-Driven testing from csv file
    @data(*Utils.read_data_from_csv("C:\\python-selenium\\TestFrameworkDemo\\testdata\\tdata_csv.csv"))
    @unpack
    def test_search_flights_1_stop(self, departlocation, goingtolocation, departuredate, stop_count):
        # Step 1: Search for flights
        search_flight_result = self.lp.searchFlights(departlocation, goingtolocation, departuredate)
        self.lp.page_scroll()

        # Step 2: Apply the stop filter dynamically
        search_flight_result.filter_flights_by_stops(stop_count)

        # Step 3: Wait for filtered results to load dynamically
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, f"//span[contains(normalize-space(text()), '{stop_count}')]")))

        # Step 4: Get all displayed flights matching the selected stop count
        all_stop_flights = self.driver.find_elements(By.XPATH,
                                                     f"//span[contains(normalize-space(text()), '{stop_count}')]")

        # Step 5: Filter out elements with empty or incomplete text
        valid_stop_flights = [flight for flight in all_stop_flights if flight.text.strip()]

        # Verify all the flights
        for flight in valid_stop_flights:
            print(f"Flight details: {flight.text}")

        # Step 6: Verify that flights exist after filtering
        assert len(valid_stop_flights) > 0, f"❌ No flights found after applying the {stop_count} filter."

        # Step 7: Print the number of filtered flights
        print(f"✅ Flights found with {stop_count}: {len(valid_stop_flights)}")

        # Step 8: Verify that each flight matches the selected stop count
        for flight in valid_stop_flights:
            assert stop_count in flight.text, f"❌ A flight does not match the filter {stop_count}. Flight details: {flight.text}"

        # Intentional failure for specific stop_count values
        if stop_count == "2 Stop":  # Fail if stop_count is 2
            assert False, f"❌ Intentional failure for stop_count = {stop_count} to test screenshot functionality."

        print(f"✅ Test Passed: All displayed flights have {stop_count}.")