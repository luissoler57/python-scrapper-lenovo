from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import os
import tempfile

print("Starting the script...")

# ! Configura las opciones de Chrome
# Ejecutar el modo sin cabeza(sin interfaz grafica)
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument(
    "--disable-dev-shm-usage"
)  # Solucionar error de memoria compartida

# ! Directorio único para datos de usuarios
user_data_dir = os.path.join(tempfile.gettempdir(), "chrome_user_data")

os.makedirs(user_data_dir, exist_ok=True)  # Crear directorio si no existe

# Agregar la ruta del directorio de datos de usuario
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

os.chmod(user_data_dir, 0o755)  # Permisos: rwxr-xr-x (755)

try:
    # Instalar/actualizar ChromeDriver automaticamente y obtener la ruta
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    driver.get("https://www.google.com")
    time.sleep(5)

    print(driver.title)

    driver.quit()
except Exception as e:
    print(f"Error: {e}")
