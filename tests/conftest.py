import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="function")
def driver():
    """
    Fixture para inicializar y cerrar el navegador Chrome.
    Se ejecuta de forma automática para cada función de prueba.
    """
    # 1. Configuración de opciones de Chrome
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Abre el navegador maximizado
    chrome_options.add_argument("--incognito")        # Abre en modo incógnito para evitar problemas de cookies/caché
    
    # Descomentar la siguiente línea si en el futuro querés correr los tests en segundo plano (sin interfaz gráfica)
    # chrome_options.add_argument("--headless=new") 

    # 2. Inicialización del WebDriver (Setup)
    # En Selenium 4+, ya no es obligatorio especificar la ruta del chromedriver
    driver = webdriver.Chrome(options=chrome_options)
    
    # 3. Entrega del driver al test
    yield driver
    
    # 4. Limpieza post-prueba (Teardown)
    # Este bloque se ejecuta SI O SI, incluso si la prueba falla.
    driver.quit()