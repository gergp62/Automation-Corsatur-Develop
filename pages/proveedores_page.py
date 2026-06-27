from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class ProveedoresPage(BasePage):
    """
    Page Object Model para el módulo de Directorio de Proveedores Turísticos.
    """

    # =========================================================================
    # LOCALIZADORES
    # =========================================================================
    BOTON_VER_PROVEEDORES = (By.XPATH, "//button[contains(., 'Ver proveedores')]")
    
    # Cambiamos el SVG genérico por el botón exacto de la primera fila de la tabla
    ICONO_VER_PRIMER_DETALLE = (By.XPATH, "//table/tbody/tr[1]/td[4]//button")
    
    # Botón Volver exacto provisto por la estructura de Material-UI
    BOTON_VOLVER = (By.XPATH, "//button[contains(., 'Volver')]")
    
    CUERPO_PAGINA = (By.TAG_NAME, "body")

    # =========================================================================
    # MÉTODOS DE INTERACCIÓN
    # =========================================================================
    def ir_a_directorio_proveedores(self):
        """Hace clic en la tarjeta/botón de la página de inicio."""
        self.hacer_clic(self.BOTON_VER_PROVEEDORES)

    def ver_primer_proveedor(self):
        """Hace clic en el ícono del ojo del primer registro de la lista."""
        self.hacer_clic(self.ICONO_VER_PRIMER_DETALLE)

    def volver_al_listado(self):
        """Regresa a la pantalla del listado general."""
        self.hacer_clic(self.BOTON_VOLVER)

    def esperar_presencia_de_texto(self, texto_esperado: str, timeout=10) -> bool:
        """Detiene la prueba hasta que el texto indicado aparezca en el DOM."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(self.CUERPO_PAGINA, texto_esperado)
            )
            return True
        except Exception:
            return False

    def obtener_texto_completo(self) -> str:
        """Devuelve todo el texto visible en pantalla para aserciones secundarias."""
        return self.driver.find_element(*self.CUERPO_PAGINA).text