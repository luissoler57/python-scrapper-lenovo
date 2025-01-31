"""_summary_
Raises:
    TypeError: _description_
Returns:
    _type_: _description_
"""

from typing import Dict, List, Optional

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

    def perform_search(self, serial: str, search_text: str):
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

            # Find the navigation item
            selected_nav = self.data_warranty_servicie(
                driver=self.driver, search_text=search_text, nav_data=data_nav
            )

            return selected_nav

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

    def find_nav_item(
        self,
        search_text: str,
        nav_data: list,
        find_first: bool = True,
        case_sensitive: bool = False,
        exact_match: bool = True,
        debug=False,
    ) -> Optional[List[Dict]]:
        """
        Busca coincidencias de texto en los datos de navegación.
        Args:
            search_text (str): Texto a buscar
            nav_data (list): Datos de navegación de extract_nav_data()
            find_first (bool): True para devolver solo el primer resultado        case_sensitive (bool): True para búsqueda sensible a mayúsculas
            exact_match (bool): True para coincidencia exacta, False para parcial
        Returns:
            Optional[List[Dict]]: Lista de coincidencias (vacía si no hay)
        """
        if not isinstance(nav_data, list):
            # Raise desencadena una excepcion controlada
            raise TypeError("nav_data debe ser una lista de diccionarios")
        processed_search = search_text.strip()
        if not case_sensitive:
            processed_search = processed_search.lower()
        matches = []
        for item in nav_data:
            try:
                item_text = str(item.get("text", "")).strip()
            except AttributeError:
                continue
            if debug:
                print(f"[DEBUG] Item: {item_text}")
            # Si el case_sensitive es False, convertir a minúsculas si no el texto original
            compare_text = item_text if case_sensitive else item_text.lower()
            if exact_match:
                # Si requiere coinicidencia exacta
                match = compare_text == processed_search
            else:
                # Si requiere coincidencia parcial
                match = processed_search in compare_text
            if match:
                if find_first:
                    return [item]
                matches.append(item)

        return matches if matches else None

    def data_warranty_servicie(
        self, driver, search_text: str, nav_data: list
    ) -> Optional[List[dict]]:

        data_warranty = []
        warranties = []

        try:
            selected_nav = self.find_nav_item(
                search_text=search_text, nav_data=nav_data
            )

            driver.get(selected_nav[0].get("href"))

            title_sube_menu = driver.find_element(
                By.CSS_SELECTOR, "div.header__content"
            ).get_attribute("innerText")

            model_found = driver.find_element(
                By.CSS_SELECTOR, "div.prod-name"
            ).get_attribute("innerText")

            # Extract the warranty details

            warranty_containers = driver.find_elements(
                By.CSS_SELECTOR, "div.cell-detail"
            )

            for container in warranty_containers:
                warranty_data = {}

                # Extract the warr4anty title
                warranty_title = container.find_element(
                    By.CSS_SELECTOR, "span.title-content"
                ).get_attribute("innerText")

                # Set the warranty title
                warranty_data["title"] = warranty_title

                # Click the icon to expand the warranty details
                if not container == warranty_containers[0]:
                    i_icon = container.find_element(
                        By.CSS_SELECTOR, "div.detail-title > i"
                    )
                    driver.execute_script("arguments[0].click();", i_icon)

                properties = container.find_elements(
                    By.CSS_SELECTOR, "div.detail-property"
                )
                for prop in properties:
                    key = prop.find_element(
                        By.CSS_SELECTOR, "span.property-title"
                    ).text.strip(":")
                    value = prop.find_element(
                        By.CSS_SELECTOR, "span.property-value"
                    ).text
                    warranty_data[key] = value

                # Extraer la descripción (si existe)
                try:
                    description = container.find_element(
                        By.CSS_SELECTOR, "p.content-description"
                    ).text
                    warranty_data["description"] = description
                except NoSuchElementException:
                    warranty_data["description"] = "No description available"

                # Add the warranty details to the dictionary
                warranties.append(warranty_data)

            data_warranty = [
                {
                    "Title ": title_sube_menu,
                    "URL": selected_nav[0].get("href"),
                    "Model": model_found,
                    "type_warranty": warranties,
                }
            ]

        except Exception as e:
            self.logger.error("Error al buscar el elemento de navegación: %s", str(e))
            raise

        return data_warranty
