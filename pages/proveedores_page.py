import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class ProveedoresPage(BasePage):
    # Selector robusto: busca cualquier botón que contenga un SVG (el ícono del ojo)
    ICONO_VER_PRIMER_DETALLE = (By.XPATH, "(//button[.//svg])[1]")
    BOTON_VOLVER = (By.XPATH, "//button[contains(text(), 'Volver')]")
    CUERPO_PAGINA = (By.TAG_NAME, "body")

    def hacer_clic_seguro(self, locator):
        """
        Espera activa: primero asegura que el elemento exista, 
        luego que sea clickeable, y hace scroll.
        """
        wait = WebDriverWait(self.driver, 15) # Aumentamos tiempo a 15s
        elemento = wait.until(EC.element_to_be_clickable(locator))
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
        elemento.click()

    def ver_primer_proveedor(self):
        """
        Esta es la parte clave: después de filtrar, la página necesita
        unos milisegundos para renderizar el botón final.
        """
        time.sleep(2) # Pausa obligatoria para que el filtro termine de pintar la grilla
        self.hacer_clic_seguro(self.ICONO_VER_PRIMER_DETALLE)

    def volver_al_listado(self):
        self.hacer_clic_seguro(self.BOTON_VOLVER)
        time.sleep(1)