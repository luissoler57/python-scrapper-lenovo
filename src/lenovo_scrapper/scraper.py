from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .utils.logger import configure_logger


class LenovoWarrantyScraper:
    def __init__(self, driver, settings, selectors):
        self.driver = driver
        self.setting = settings
        self.selectors = selectors
        self.logger = configure_logger("scraper")

    def perform_search(self, serial: str):
        """Perform a search for the given serial number and return the product name."""
        try:
            self.driver.get(self.setting.BASE_URL)
            search_box = WebDriverWait(self.driver, self.setting.DEFAULT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, self.selectors.SEARCH_INPUT)
                )
            )
            search_box.send_keys(serial + Keys.ENTER)

            title = self.driver.find_element(
                By.CSS_SELECTOR, self.selectors.PRODUCT_NAME
            )

            return title.text

        except WebDriverException as e:
            self.logger.error("Search error: %s", str(e))
            raise
