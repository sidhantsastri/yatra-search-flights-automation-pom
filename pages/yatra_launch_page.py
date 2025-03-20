import logging
import time
import datetime
from selenium.webdriver.common.by import By
from base.base_driver import BaseDriver
from pages.search_flights_results_page import SearchFlightResults
from utilities.utils import Utils

class LaunchPage(BaseDriver):
    # use the custom logger at the class level
    log = Utils.custum_logger()
    def __init__(self, driver):
        # Calls the constructor of the parent base_driver class
        super().__init__(driver) # Inherit driver and wait setup from BaseDriver
        #self.driver = driver

    # Locators
    # Externalised the location / get the xpath for depart from
    DEPART_FROM_FIELD ="//p[normalize-space()='new delhi']"
    DEPART_FROM_CITY = "//input[@id='input-with-icon-adornment']"
    GET_FIRST_OPTION = "//li[@class='css-1546kn3']"
    # get the xpath from going to
    GOING_TO_FIELD = "//p[@title='Mumbai']"
    GOING_TO_AUTO = "//input[@id='input-with-icon-adornment']"
    SEARCH_RESULTS = "//ul//li[contains(@class, 'css-1546kn3')]"
    # Select xpath of departure date calendar
    OPEN_CALENDAR = "//div[@class='css-w7k25o']"
    DISMISS_OVERLAY = "MuiBackdrop-root"
    CALENDAR_VISIBLE = "//div[contains(@class,'dual-calendar')]//div[contains(@class,'react-datepicker__day') and not(contains(@class,'react-datepicker__day--disabled'))]//span"



    #DATE_CONTAINER = "./ancestor::div[contains(@class,'react-datepicker__day')]"
    # Select xpath for search result btn
    SEARCH_BUTTON_CLICK = "//button[normalize-space()='Search']"

    # Define the method here
    # Get the depart from field and click / Enter departure city / Select first suggestion from dropdown
    def getDepartFromField(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.DEPART_FROM_FIELD)
    def getDepartFromCity(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.DEPART_FROM_CITY)
    def getFirstOption(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.GET_FIRST_OPTION)

    # return xpath for going to field
    def getGoingToField(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.GOING_TO_FIELD)
    def getGoingToAuto(self):
        return self.wait_until_visibility_of_the_element(By.XPATH, self.GOING_TO_AUTO)
    def getSearchResults(self):
        return self.wait_for_the_presence_of_all_elements(By.XPATH, self.SEARCH_RESULTS)

    # Return xpath for the departure date calendar
    def getcalendar(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.OPEN_CALENDAR)
    def dismissoverlay(self):
        return self.wait_until_invisibility_of_the_element(By.XPATH, self.DISMISS_OVERLAY)
    def calendarvisibility(self):
        return self.wait_for_the_presence_of_all_elements(By.XPATH, self.CALENDAR_VISIBLE)

    # Return xpath for search btn
    def searchbtnclick(self):
        return self.wait_until_element_is_clickable(By.XPATH, self.SEARCH_BUTTON_CLICK)

    # Do operations here
    # Click on the field/ Type on it / Send keys
    def enterDepartFromLocation(self, departlocation):
        self.getDepartFromField().click()
        self.getDepartFromCity().send_keys(departlocation)
        self.getFirstOption().click()

    # Going to field
    def enterGoingToLocation(self, goingToLocation):
        self.getGoingToField().click()
        self.getGoingToAuto().send_keys(goingToLocation)
        time.sleep(2)
        search_results = self.getSearchResults()
        for result in search_results:
            self.log.info(result.text)
            if "New York, (JFK)" in result.text:
                # Use explicit wait to ensure the element is clickable
                self.click_when_clickable(result)
                break

    # Perform actions for departure date calendar
    def selectDepartureDate(self, departuredate):
        self.getcalendar().click()
        self.dismissoverlay()

        # If only "March 28" is provided, append the current year
        if len(departuredate.split()) == 2:
            current_year = datetime.datetime.now().year
            departuredate += f" {current_year}"

        # Convert to datetime object
        departure_dt = datetime.datetime.strptime(departuredate, "%d %B %Y")

        # Format date for the website
        day_with_suffix = departure_dt.strftime("%d").lstrip("0") + (
            "st" if departure_dt.day in [1, 21, 31] else
            "nd" if departure_dt.day in [2, 22] else
            "rd" if departure_dt.day in [3, 23] else "th"
        )

        # **Updated format to match "Choose Friday, March 28th, 2025"**
        formatted_date = f"Choose {departure_dt.strftime('%A, %B')} {day_with_suffix}, {departure_dt.year}"

        self.log.info(f"Looking for date: {formatted_date}")

        # Construct a dynamic XPath that targets the correct month and day
        DATE_CONTAINER = f"//div[contains(@class,'react-datepicker__month')]//div[contains(@aria-label, '{formatted_date}')]"

        all_dates = self.calendarvisibility()
        for date in all_dates:
            date_container = date.find_element(By.XPATH, DATE_CONTAINER)
            aria_label = date_container.get_attribute("aria-label")
            date_text = date_container.text.strip()
            self.log.info(f"Checking: {date_text} | Aria-label: {aria_label}")  # Debugging step
            if formatted_date in aria_label:
                date_container.click()
                break
        time.sleep(4)

    # CLick on the search results btn
    def clickSearchBtn(self):
        self.searchbtnclick().click()
        time.sleep(4)

    def searchFlights(self, departlocation,goingtolocation, departuredate):
        self.enterDepartFromLocation(departlocation)
        self.enterGoingToLocation(goingtolocation)
        self.selectDepartureDate(departuredate)
        self.clickSearchBtn()
        # It navigates to search flights results page - so create the object of the search_flights_results_page and return the value
        search_flights_results = SearchFlightResults(self.driver)
        return search_flights_results

    # def departfrom(self, departlocation):
    #     # Click on "Depart From" field
    #     depart_from = self.wait_until_element_is_clickable(By.XPATH, "//p[normalize-space()='new delhi']")
    #     depart_from.click()
    #     # Enter departure city
    #     depart_auto = self.wait_until_element_is_clickable(By.XPATH, "//input[@id='input-with-icon-adornment']")
    #     depart_auto.send_keys(departlocation)
    #     # Select the first suggestion from dropdown
    #     first_option = self.wait_until_element_is_clickable(By.XPATH, "//li[@class='css-1546kn3']")
    #     first_option.click()

    # def goingto(self,goingtolocation):
    #     # **Explicit wait for "Going To" field before clicking**
    #     going_to = self.wait_until_element_is_clickable(By.XPATH, "//p[@title='Mumbai']")
    #     going_to.click()
    #     # Wait for input field to be visible before sending keys
    #     going_auto = self.wait_until_visibility_of_the_element(By.XPATH, "//input[@id='input-with-icon-adornment']")
    #     going_auto.send_keys(goingtolocation)
    #     # Wait for dropdown options to load completely
    #     time.sleep(2)  # Short pause for options to load (reduces race condition)
    #     # Retrieve all dropdown options
    #     search_results = self.wait_for_the_presence_of_all_elements(By.XPATH, "//ul//li[contains(@class, 'css-1546kn3')]")
    #     # print("Number of suggestions:", len(search_results))
    #     # Loop through results and click on "New York, (JFK)"
    #     for result in search_results:
    #         # print(result.text)
    #         if "New York, (JFK)" in result.text:
    #             # Use explicit wait to ensure the element is clickable
    #             self.click_when_clickable(result)
    #             break

    # def selectdate(self,departuredate):
    #     calendar = self.wait_until_element_is_clickable(By.XPATH, "//div[@class='css-w7k25o']")
    #     calendar.click()
    #     # Wait for any overlay or modal to disappear
    #     self.wait_until_invisibility_of_the_element(By.CLASS_NAME, "MuiBackdrop-root")
    #     # Wait for calendar to be visible
    #     all_dates = self.wait_for_the_presence_of_all_elements(By.XPATH,
    #                                                                      "//div[contains(@class,'dual-calendar')]//div[contains(@class,'react-datepicker__day') and not(contains(@class,'react-datepicker__day--disabled'))]//span")
    #
    #     for date in all_dates:
    #         date_container = date.find_element(By.XPATH, "./ancestor::div[contains(@class,'react-datepicker__day')]")
    #         aria_label = date_container.get_attribute("aria-label")
    #         date_text = date.text.strip()
    #         print("Date:", date_text, "| Aria-label:", aria_label)  # Debugging step
    #         if departuredate in aria_label:
    #             date_container.click()
    #             break
    #     time.sleep(4)

    # Search button click
    # def clicksearch(self):
    #     search_btn = self.wait_until_element_is_clickable(By.XPATH, "//button[normalize-space()='Search']")
    #     search_btn.click()
    #     time.sleep(3)