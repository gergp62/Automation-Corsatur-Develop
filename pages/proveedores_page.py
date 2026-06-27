import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException, ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys
from .base_page import BasePage

class ProveedoresPage(BasePage):
    """
    Page Object Model unificado y blindado para el módulo de Proveedores Turísticos.
    Resuelve problemas de asincronismo mediante una estrategia polimórfica de selectores.
    """

    # =========================================================================
    # LOCALIZADORES
    # =========================================================================
    BOTON_VER_PROVEEDORES = (By.XPATH, "//button[contains(., 'Ver proveedores')]")
    CUERPO_PAGINA = (By.TAG_NAME, "body")
    BUSCADOR_TEXTO = (By.XPATH, "//input[@id='search-input' or contains(@placeholder, 'Buscar')]")
    
    # Elementos del Modal de Filtros
    BOTON_ABRIR_FILTROS = (By.XPATH, "//button[contains(., 'Filtros')]")
    BOTON_APLICAR_FILTROS = (By.XPATH, "//button[contains(., 'Aplicar filtros') or contains(., 'Aplicar')]")
    
    # Selectores Dropdown (Componentes Material-UI)
    COMBO_PAIS = (By.XPATH, "//p[contains(text(), 'Seleccionar país') or contains(., 'País')]")
    COMBO_REGION = (By.XPATH, "//p[contains(text(), 'Seleccionar región') or contains(text(), 'Seleccionar region') or contains(., 'Región')]")
    COMBO_DEPARTAMENTO = (By.XPATH, "//p[contains(text(), 'Seleccionar departamento') or contains(., 'Departamento')]")
    COMBO_MUNICIPIO = (By.XPATH, "//p[contains(text(), 'Seleccionar municipio') or contains(., 'Municipio')]")
    COMBO_DISTRITO = (By.XPATH, "//p[contains(text(), 'Seleccionar distrito') or contains(., 'Distrito')]")

    # Botón Volver de la vista interna
    BOTON_VOLVER = (By.XPATH, "//button[contains(., 'Volver')]")

    # =========================================================================
    # MÉTODOS DE INTERACCIÓN GENERAL Y BÚSQUEDA
    # =========================================================================
    def ir_a_directorio_proveedores(self):
        """Navega desde la home hacia el listado de proveedores"""
        self.hacer_clic(self.BOTON_VER_PROVEEDORES)
        time.sleep(2.0)  # Asentamiento para renderizar la grilla inicial

    def abrir_modal_filtros(self):
        self.hacer_clic_seguro(self.BOTON_ABRIR_FILTROS)
        time.sleep(0.5)

    def buscar_en_barra(self, texto: str):
        """Ingresa texto en la barra absorbiendo el tiempo de debounce de la búsqueda reactiva"""
        self.escribir(self.BUSCADOR_TEXTO, texto)
        time.sleep(3.0)  # Pausa crítica: permite que el input reactive termine de mutar el DOM

    # =========================================================================
    # EL NÚCLEO DE LA SOLUCIÓN: ESTRATEGIA POLIMÓRFICA PARA EL "OJO"
    # =========================================================================
    def ver_primer_proveedor(self):
        """
        Prueba dinámicamente múltiples XPaths para capturar el botón de 'Ver detalle'.
        Evita los Timeouts fijos y asegura el clic de forma nativa o por JavaScript.
        """
        time.sleep(3.0)  # Amortiguación obligatoria ante actualizaciones de grilla o cierres de modal

        # Lista de XPaths ordenados por precisión técnica para interactuar con la primera fila
        ESTRATEGIAS_XPATH = [
            "//table/tbody/tr[1]/td[4]//button",                                 # Estructura de tabla tradicional (Fila 1, Columna 4)
            "(//button[descendant::svg])[1]",                                    # Cualquier botón con un icono SVG adentro (El Ojo)
            "(//button[contains(@class, 'MuiButton') or @type='button'])[1]",    # El primer botón interactivo de la sección de datos
            "(//tbody//button)[1]",                                              # El primer botón que exista dentro de un cuerpo de tabla
            "(//*[contains(@class, 'cell')]//button)[1]",                        # Botón dentro de una celda con clase CSS común de grillas
            "(//button)[1]"                                                      # Fallback extremo: el primer botón del layout de resultados
        ]

        elemento_ojo = None
        
        # Barrido veloz de estrategias sin esperas ciegas de 12 segundos
        for xpath in ESTRATEGIAS_XPATH:
            try:
                elementos = self.driver.find_elements(By.XPATH, xpath)
                if elementos and elementos[0].is_displayed():
                    elemento_ojo = elementos[0]
                    print(f"\n[DEBUG QA] -> Botón 'ojo' localizado exitosamente con el XPath: {xpath}")
                    break
            except Exception:
                continue

        # Alerta temprana antes de que explote Selenium de forma genérica
        if not elemento_ojo:
            raise Exception(
                "[ERROR CRÍTICO QA] No se pudo localizar el botón del 'ojo' con ninguna de las 6 estrategias analizadas. "
                "Verificá si la búsqueda o los filtros aplicados están dejando la grilla totalmente vacía (0 resultados)."
            )

        # Ejecución blindada del clic
        try:
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_ojo)
            time.sleep(0.3)
            elemento_ojo.click()
        except Exception:
            # Fallback inmediato por JS si el elemento está tapado por algún overlay invisible de Material-UI
            self.driver.execute_script("arguments[0].click();", elemento_ojo)
        
        time.sleep(2.0)  # Espera para que comience la transición hacia la vista de detalle

    def volver_al_listado(self):
        self.hacer_clic_seguro(self.BOTON_VOLVER)
        time.sleep(1.5)

    # =========================================================================
    # MECANISMOS DE SOPORTE PARA FILTROS AVANZADOS (MATERIAL-UI)
    # =========================================================================
    def hacer_clic_seguro(self, locator, timeout=10):
        """Asegura la interacción sorteando problemas de interceptación o elementos inestables"""
        wait = WebDriverWait(self.driver, timeout)
        for _ in range(3):
            try:
                elemento = wait.until(EC.element_to_be_clickable(locator))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
                elemento.click()
                return
            except (StaleElementReferenceException, ElementClickInterceptedException):
                time.sleep(0.8)
        
        # Fallback por JS si los reintentos fallan
        elemento_fallback = self.driver.find_element(*locator)
        self.driver.execute_script("arguments[0].click();", elemento_fallback)

    def _seleccionar_opcion_mui(self, locator_combo, texto_opcion, timeout=8):
        """Manejador genérico e insensible a mayúsculas/acentos para drop-downs de Material-UI"""
        texto_lower = texto_opcion.lower()
        xpath_case_insensitive = (
            f"//li["
            f"contains(translate(text(), 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ', 'abcdefghijklmnñopqrstuvwxyzáéíóú'), '{texto_lower}') "
            f"or contains(translate(., 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ', 'abcdefghijklmnñopqrstuvwxyzáéíóú'), '{texto_lower}')"
            f"]"
        )
        locator_opcion = (By.XPATH, xpath_case_insensitive)
        end_time = time.monotonic() + timeout
        
        while time.monotonic() < end_time:
            self.hacer_clic_seguro(locator_combo)
            time.sleep(0.5)
            
            elementos = self.driver.find_elements(*locator_opcion)
            if any(el.is_displayed() for el in elementos):
                self.hacer_clic_seguro(locator_opcion)
                time.sleep(0.5)
                return
                
            listboxes = self.driver.find_elements(By.XPATH, "//ul[@role='listbox'] | //div[contains(@class, 'MuiMenu-paper')]")
            if any(lb.is_displayed() for lb in listboxes):
                try:
                    WebDriverWait(self.driver, 2.5).until(EC.visibility_of_element_located(locator_opcion))
                    self.hacer_clic_seguro(locator_opcion)
                    time.sleep(0.5)
                    return
                except:
                    self.driver.find_element(*self.CUERPO_PAGINA).send_keys(Keys.ESCAPE)
                    time.sleep(0.3)
                    
        raise TimeoutException(f"No se pudo interactuar con la opción del dropdown: '{texto_opcion}'.")

    def seleccionar_tipo_proveedor_boton(self, tipo_proveedor):
        """Selecciona el chip o botón según la categoría de proveedor elegida"""
        tipo_lower = tipo_proveedor.lower()
        xpath_btn = (
            f"//*[(self::button or @role='button' or contains(@class, 'Chip') or self::span) and "
            f"contains(translate(., 'ABCDEFGHIJKLMNÑOPQRSTUVWXYZÁÉÍÓÚ', 'abcdefghijklmnñopqrstuvwxyzáéíóú'), '{tipo_lower}')]"
        )
        locator_btn = (By.XPATH, xpath_btn)
        self.hacer_clic_seguro(locator_btn)
        time.sleep(0.3)

    def aplicar_filtros(self):
        self.hacer_clic_seguro(self.BOTON_APLICAR_FILTROS)

    def filtrar_proveedores_avanzado(self, pais=None, region=None, departamento=None, municipio=None, distrito=None, tipo_proveedor=None):
        """Orquesta secuencialmente el formulario de filtros avanzados de 5 niveles en el modal"""
        self.abrir_modal_filtros()
        if pais:
            self._seleccionar_opcion_mui(self.COMBO_PAIS, pais)
        if region:
            self._seleccionar_opcion_mui(self.COMBO_REGION, region)
        if departamento:
            self._seleccionar_opcion_mui(self.COMBO_DEPARTAMENTO, departamento)
        if municipio:
            self._seleccionar_opcion_mui(self.COMBO_MUNICIPIO, municipio)
        if distrito:
            self._seleccionar_opcion_mui(self.COMBO_DISTRITO, distrito)
        if tipo_proveedor:
            self.seleccionar_tipo_proveedor_boton(tipo_proveedor)
        self.aplicar_filtros()

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