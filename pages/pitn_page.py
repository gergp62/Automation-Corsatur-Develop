import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from .base_page import BasePage

class PitnPage(BasePage):
    """
    Page Object Model para el módulo de Proyectos de Interés Turístico (PITN).
    """

    # =========================================================================
    # LOCALIZADORES
    # =========================================================================
    CUERPO_PAGINA = (By.TAG_NAME, "body")
    BARRA_BUSQUEDA = (By.XPATH, "//input[contains(@placeholder, 'Buscar por')]")
    BOTON_ABRIR_FILTROS = (By.XPATH, "//button[contains(., 'Filtros') or contains(., 'filtros')]")
    BOTON_APLICAR_FILTROS = (By.XPATH, "//button[contains(text(), 'Aplicar') or contains(., 'Aplicar')]")
    FILAS_GRID = (By.XPATH, "//table//tbody//tr | //div[contains(@class, 'card')] | //div[contains(@class, 'row')]")

    # =========================================================================
    # MÉTODOS DE NAVEGACIÓN E INTERACCIÓN
    # =========================================================================
    def ir_a_vista_pitn(self):
        """Navega de forma anclada a la tarjeta específica de PITN."""
        time.sleep(2.0)
        
        ESTRATEGIAS_PITN = [
            "//div[contains(., 'PITN')]/following-sibling::button[contains(., 'proyectos') or contains(., 'Conoce')]",
            "//*[contains(text(), 'PITN')]/following-sibling::*//button",
            "(//button[contains(., 'Conoce los proyectos')])[1]"
        ]

        elemento_boton = None
        for xpath in ESTRATEGIAS_PITN:
            try:
                elementos = self.driver.find_elements(By.XPATH, xpath)
                if elementos and elementos[0].is_displayed():
                    elemento_boton = elementos[0]
                    print(f"\n[DEBUG QA] -> Botón PITN hallado vía: {xpath}")
                    break
            except Exception:
                continue

        if not elemento_boton:
            raise Exception("[ERROR CRÍTICO QA] No se encontró el botón de la tarjeta PITN en la Home.")

        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_boton)
        time.sleep(0.3)
        elemento_boton.click()
        time.sleep(2.5)

    def buscar_en_barra(self, texto: str):
        """Escribe en la barra de búsqueda asegurando el foco y visibilidad del elemento."""
        wait = WebDriverWait(self.driver, 15)
        input_buscar = wait.until(EC.element_to_be_clickable(self.BARRA_BUSQUEDA))
        
        self.driver.execute_script("arguments[0].focus();", input_buscar)
        input_buscar.send_keys(Keys.CONTROL + "a")
        input_buscar.send_keys(Keys.BACKSPACE)
        time.sleep(0.5)
        
        if texto:
            input_buscar.send_keys(texto)
            input_buscar.send_keys(Keys.ENTER)
        time.sleep(3.0)

    def abrir_panel_filtros(self):
        """Hace clic en el botón principal para desplegar el menú lateral de filtros."""
        self.hacer_clic_seguro(self.BOTON_ABRIR_FILTROS)
        time.sleep(2.0)

    def seleccionar_chip_filtro(self, nombre_filtro: str):
        """Selecciona un chip interactuando con coincidencia de texto estricta."""
        print(f"[DEBUG QA] -> Forzando clic en chip: {nombre_filtro}")
        
        estrategias_chip = [
            f"//button[text()='{nombre_filtro}']",
            f"//span[text()='{nombre_filtro}']",
            f"//*[contains(@class, 'chip')]//*[text()='{nombre_filtro}']",
            f"//button[contains(., '{nombre_filtro}') and not(contains(., 'Alimentación'))]" if nombre_filtro == "Alojamiento" else f"//button[contains(., '{nombre_filtro}')]"
        ]
        
        elemento_target = None
        for xpath in estrategias_chip:
            try:
                elementos = self.driver.find_elements(By.XPATH, xpath)
                for el in elementos:
                    if el.is_displayed():
                        elemento_target = el
                        break
                if elemento_target:
                    break
            except Exception:
                continue
                
        if elemento_target:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_target)
            self.driver.execute_script("arguments[0].click();", elemento_target)
            time.sleep(0.6)
        else:
            print(f"[ALERTA QA] No se localizó visualmente el chip: {nombre_filtro}")

    def aplicar_filtros_laterales(self):
        """Aplica las selecciones realizadas en el menú lateral."""
        print("[DEBUG QA] -> Haciendo clic en Aplicar filtros...")
        btn = self.driver.find_element(*self.BOTON_APLICAR_FILTROS)
        self.driver.execute_script("arguments[0].click();", btn)
        time.sleep(2.5)
        try:
            self.driver.find_element(*self.CUERPO_PAGINA).send_keys(Keys.ESCAPE)
            time.sleep(1.0)
        except Exception:
            pass

    def verificar_grilla_con_datos(self) -> bool:
        """Devuelve True si hay elementos visibles en la grilla del listado."""
        try:
            elementos = self.driver.find_elements(*self.FILAS_GRID)
            return len(elementos) > 0
        except Exception:
            return False

    def hacer_clic_seguro(self, locator, timeout=10):
        wait = WebDriverWait(self.driver, timeout)
        for _ in range(3):
            try:
                elemento = wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
                elemento.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                time.sleep(0.8)
        
        elemento_fallback = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", elemento_fallback)

    def esperar_presencia_de_texto(self, texto_esperado: str, timeout=12) -> bool:
        """Saca el texto del DOM, lo pasa a minúsculas y busca de forma tolerante."""
        limite = time.time() + timeout
        texto_busqueda = texto_esperado.lower()
        
        while time.time() < limite:
            try:
                cuerpo = self.driver.find_element(*self.CUERPO_PAGINA)
                if texto_busqueda in cuerpo.text.lower():
                    return True
            except Exception:
                pass
            time.sleep(0.5)
        return False