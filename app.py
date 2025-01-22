from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
import tempfile

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

driver.get("https://pcsupport.lenovo.com/us/en/")

# ! Iniciar scrapper
try:
    time.sleep(10)
    # test = driver.find_element(By.CLASS_NAME, "el-input el-input--suffix")

    print(driver.title)

    # search_input = driver.find_element(By.XPATH, "//input")

    html_update = driver.execute_script("return document.documentElement.outerHTML")

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.CSS_SELECTOR, "input[type='text']"),
        ),
        "No se encontro el elemento",
    )

    with open("./page_complete.html", "w") as file:
        file.write(html_update)

    print(search_box.get_attribute("outerHTML"))
    driver.quit()
except Exception as e:
    print(f"Error: {e}")
