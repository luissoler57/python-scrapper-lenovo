from selenium.common.exceptions import (
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
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

            # Extract navigation data
            data_nav = self.extract_nav_data()

            return data_nav

        except WebDriverException as e:
            self.logger.error("Search error: %s", str(e))
            raise

    def extract_nav_data(self):
        """
        Extrae datos de navegación de un controlador web.
        Args:
            driver (WebDriver): El controlador web de Selenium.
        Returns:
            list: Una lista de diccionarios con los datos de navegación extraídos.
            Cada diccionario contiene las siguientes claves:
                - "text" (str): El texto del elemento de navegación.
                - "href" (str): El enlace del elemento de navegación.
                - "is_active" (bool): Indica si el elemento de navegación está activo.
        Raises:
            Exception: Si ocurre un error al extraer un elemento de navegación,
            se captura y se imprime el error, y la extracción continúa con el siguiente elemento.
        """

        WebDriverWait(self.driver, 1).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "ul.main-navigation"),
            )
        )

        items = self.driver.find_elements(
            By.CSS_SELECTOR, self.selectors.MAIN_NAVIGATION
        )

        data = []

        for item in items:

            try:

                # Extract the link
                link_element = item.find_element(By.CSS_SELECTOR, "a.vue-nav-menu")
                href = link_element.get_attribute("href")
                text_span = link_element.find_element(
                    By.CSS_SELECTOR, "span.tab-display-name"
                )
                data.append(
                    {
                        "text": text_span.get_attribute("innerText"),
                        "href": href,
                        "is_active": "active" in item.get_attribute("class"),
                    }
                )

            except (NoSuchElementException, TimeoutException) as e:
                self.logger.ERROR(f"Error extrayento item:  {str(e)}")
                continue

        return data
