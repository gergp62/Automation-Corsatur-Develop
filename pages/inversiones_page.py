import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
from .base_page import BasePage

class InversionesPage(BasePage):
    """
    Page Object Model exclusivo para el módulo de Inversiones Públicas.
    Maneja la navegación desde la Home y las interacciones internas del sector.
    """

    # =========================================================================
    # LOCALIZADORES
    # =========================================================================
    CUERPO_PAGINA = (By.TAG_NAME, "body")
    BOTON_INVERTIR_SV = (By.XPATH, "//button[contains(., 'Invertir en El Salvador')]")
    BOTON_VOLVER = (By.XPATH, "//button[contains(., 'Volver')]")

    # =========================================================================
    # MÉTODOS DE INTERACCIÓN
    # =========================================================================
    def ir_a_vista_inversiones(self):
        """
        Navega desde la home hacia la sección de Proyectos de Inversión de forma exacta.
        Utiliza anclajes por contenedores para evitar colisiones con tarjetas vecinas.
        """
        time.sleep(2.0) # Espera de asentamiento de la Home
        
        # Estrategias que buscan explícitamente el contenedor o título de "Inversiones" antes de ir al botón
        ESTRATEGIAS_BOTON_HOME = [
            # Estrategia 1: Busca un contenedor que tenga el encabezado exacto "Inversiones" y luego su botón
            "//div[contains(., 'Inversiones')]/following-sibling::button[contains(., 'proyectos') or contains(., 'Conece')]",
            # Estrategia 2: Busca el título exacto h2/h3/p "Inversiones" y navega al botón hermano o descendiente
            "//*[text()='Inversiones']/following-sibling::*//button[contains(., 'proyectos')]",
            # Estrategia 3: Indexación directa basada en la estructura visual (Tarjeta Central = Índice 2)
            "(//button[contains(., 'Conoce los proyectos')])[2]",
            # Estrategia 4: Relación descendente estricta desde un bloque de texto identificable
            "//div[p[contains(text(), 'desarrollo de inversiones')]]//button"
        ]

        elemento_boton = None
        for xpath in ESTRATEGIAS_BOTON_HOME:
            try:
                elementos = self.driver.find_elements(By.XPATH, xpath)
                if elementos and elementos[0].is_displayed():
                    elemento_boton = elementos[0]
                    print(f"\n[DEBUG QA] -> Botón de Inversiones (Anclado) hallado con éxito vía: {xpath}")
                    break
            except Exception:
                continue

        if not elemento_boton:
            raise Exception("[ERROR CRÍTICO QA] No se encontró el botón específico de la tarjeta 'Inversiones' en la Home.")

        # Forzar clic de manera segura
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_boton)
            time.sleep(0.3)
            elemento_boton.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", elemento_boton)
            
        time.sleep(2.5)  # Tiempo prudencial para que cargue la SPA de Inversiones

    def hacer_clic_invertir_en_salvador(self):
        """Dispara el enlace externo que abrirá la nueva pestaña de gobierno"""
        self.hacer_clic_seguro(self.BOTON_INVERTIR_SV)
        time.sleep(2.5)

    def volver_a_la_home(self):
        """Hace clic en el botón Volver para regresar al dashboard/home principal"""
        self.hacer_clic_seguro(self.BOTON_VOLVER)
        time.sleep(1.5)

    # =========================================================================
    # SOPORTE ESTABILIZADOR
    # =========================================================================
    def hacer_clic_seguro(self, locator, timeout=10):
        """Asegura el clic sorteando problemas de superposición en componentes dinámicos"""
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

    def obtener_texto_completo(self) -> str:
        return self.driver.find_element(*self.CUERPO_PAGINA).text

    def esperar_presencia_de_texto(self, texto_esperado: str, timeout=12) -> bool:
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(self.CUERPO_PAGINA, texto_esperado)
            )
            return True
        except Exception:
            return False