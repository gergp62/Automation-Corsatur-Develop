from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)  # Espera máxima de 10 segundos

    def abrir_url(self, url):
        """Navega a una URL específica"""
        self.driver.get(url)

    def encontrar_elemento(self, locator):
        """Espera a que el elemento sea visible en el DOM antes de retornarlo"""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def hacer_clic(self, locator):
        """Espera a que el elemento sea cliqueable y hace clic"""
        elemento = self.wait.until(EC.element_to_be_clickable(locator))
        elemento.click()

    def escribir(self, locator, texto):
        """Espera al elemento, lo limpia e ingresa texto"""
        elemento = self.encontrar_elemento(locator)
        elemento.clear()
        elemento.send_keys(texto)
        
    def obtener_texto(self, locator):
        """Obtiene el texto de un elemento visible"""
        return self.encontrar_elemento(locator).text

    def seleccionar_por_texto(self, locator, texto):
        """Espera a que el dropdown esté listo y selecciona una opción por su texto visible"""
        elemento = self.encontrar_elemento(locator)
        select = Select(elemento)
        select.select_by_visible_text(texto)