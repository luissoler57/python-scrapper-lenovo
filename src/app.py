import os
import tempfile
from typing import List, Dict, Optional

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains

SERIAL = "PF3DGHLB"


print("Starting the script...")


# User-Agent actualizado (ej: Chrome 117 en Windows)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"


# ! Configura las opciones de Chrome

# Ejecutar el modo sin cabeza(sin interfaz grafica)

chrome_options = Options()

chrome_options.add_argument(f"user-agent={USER_AGENT}")

chrome_options.add_experimental_option(

    "excludeSwitches", ["enable-automation"])

chrome_options.add_argument("--headless")

chrome_options.add_argument("--disable-gpu")

chrome_options.add_argument("--no-sandbox")

# ? Solucionar error de memoria compartida

chrome_options.add_argument("--disable-dev-shm-usage")


# ! Directorio único para datos de usuarios

user_data_dir = os.path.join(tempfile.gettempdir(), "chrome_user_data")


os.makedirs(user_data_dir, exist_ok=True)  # Crear directorio si no existe


# Agregar la ruta del directorio de datos de usuario

chrome_options.add_argument(f"--user-data-dir={user_data_dir}")


os.chmod(user_data_dir, 0o755)  # Permisos: rwxr-xr-x (755)


# Instalar/actualizar ChromeDriver automaticamente y obtener la ruta
web_driver = webdriver.Chrome(

    service=Service(ChromeDriverManager().install()), options=chrome_options
)

web_driver.get("https://support.lenovo.com/us/en/parts-lookup")


# ! Iniciar scrapper


print("Scraping...")

search_box = WebDriverWait(web_driver, 2).until(

    EC.presence_of_element_located(
        (

            By.CSS_SELECTOR,

            "input[type='text'][placeholder='Search by product name, serial number, machine type']",

        ),

    ),

    "No se encontro el elemento",
)


search_box.send_keys(SERIAL + Keys.ENTER)


modelo_name = web_driver.find_element(
    By.CSS_SELECTOR, "div[class='prod-name']")
print()

print("MODELO: ", modelo_name.get_attribute("innerText"))
print()


# ! Extraer datos de navegación

def extract_nav_data(driver):
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

    print("Extracting data...")

    WebDriverWait(driver, 1).until(

        EC.presence_of_element_located(

            (By.CSS_SELECTOR, "ul.main-navigation"),
        )
    )

    items = driver.find_elements(

        By.CSS_SELECTOR, "ul.main-navigation > li.navtiles")

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

            print(f"Error extrayento item:  {str(e)}")
            continue

    return data


data_links = extract_nav_data(web_driver)


def find_nav_item(

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

        find_first (bool): True para devolver solo el primer resultado

        case_sensitive (bool): True para búsqueda sensible a mayúsculas

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


seleted = find_nav_item(

    search_text="Warranty & Services",

    nav_data=data_links,

    exact_match=True,

    find_first=True,
)

web_driver.get(seleted[0]["href"])

print("Current URL: ", web_driver.current_url)

sub_menu = web_driver.find_element(

    By.CSS_SELECTOR, "div.header__content")

print()

print("Redirecting to: ", sub_menu.get_attribute("innerText"))


def extract_warranty_details(driver):
    """
    Extrae los detalles de las garantías desde el HTML proporcionado.

    Args:
        driver: Instancia de Selenium WebDriver.

    Returns:
        list: Lista de diccionarios con los detalles de cada garantía.
    """
    warranties = []

    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "div.cell-detail")
        ))

    warranty_containers = driver.find_elements(
        By.CSS_SELECTOR, "div.cell-detail")

    for container in warranty_containers:
        warranty_data = {}

        # Extract the warr4anty title
        warranty_title = container.find_element(
            By.CSS_SELECTOR, "span.title-content").get_attribute("innerText")

        # Set the warranty title
        warranty_data["title"] = warranty_title

        # Click the icon to expand the warranty details
        if not container == warranty_containers[0]:
            i_icon = container.find_element(
                By.CSS_SELECTOR, "div.detail-title > i")
            driver.execute_script("arguments[0].click();", i_icon)

        properties = container.find_elements(
            By.CSS_SELECTOR, "div.detail-property")
        for prop in properties:
            key = prop.find_element(
                By.CSS_SELECTOR, "span.property-title").text.strip(":")
            value = prop.find_element(
                By.CSS_SELECTOR, "span.property-value").text
            warranty_data[key] = value

         # Extraer la descripción (si existe)
        try:
            description = container.find_element(
                By.CSS_SELECTOR, "p.content-description").text
            warranty_data["description"] = description
        except NoSuchElementException:
            warranty_data["description"] = "No description available"

        # Add the warranty details to the dictionary
        warranties.append(warranty_data)

    return warranties


print()
warranty = extract_warranty_details(web_driver)

for w in warranty:
    print(w)
    print()
print("Closing the browser...")
web_driver.quit()
