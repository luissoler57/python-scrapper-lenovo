from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
import tempfile


SERIAL = "PF3DGHLB"

print("Starting the script...")

# User-Agent actualizado (ej: Chrome 117 en Windows)
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36"

# ! Configura las opciones de Chrome
# Ejecutar el modo sin cabeza(sin interfaz grafica)
chrome_options = Options()
chrome_options.add_argument(f"user-agent={user_agent}")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
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
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=chrome_options
)

driver.get("https://support.lenovo.com/us/en/parts-lookup")

# ! Iniciar scrapper

print("Scraping...")
search_box = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(
        (
            By.CSS_SELECTOR,
            "input[type='text'][placeholder='Search by product name, serial number, machine type']",
        ),
    ),
    "No se encontro el elemento",
)

search_box.send_keys(SERIAL + Keys.ENTER)

new_page = driver.find_element(By.CSS_SELECTOR, "div[class='prod-name']")
print()
print("MODELO: ", new_page.get_attribute("innerText"))
print()


def extract_nav_data(driver):
    print("Extracting data...")

    """Extracts the navigation data from the page

    Returns:
        _type_: _description_
    """
    WebDriverWait(driver, 1).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "ul.main-navigation"),
        )
    )
    items = driver.find_elements(By.CSS_SELECTOR, "ul.main-navigation > li.navtiles")

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

        except Exception as e:
            print(f"Error extrayento item: ", {str(e)})
            continue

    return data


data_links = extract_nav_data(driver)


print("Data: ", data_links)


print("Closing the browser...")
driver.quit()
