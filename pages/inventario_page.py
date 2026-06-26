import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class InventarioPage(BasePage):
    """
    Page Object Model para el módulo de Inventario Turístico.
    Cubre la visualización, filtros de búsqueda (público/admin) y el flujo 
    de registro de empresas turísticas (HU001 y HU002).
    """

    # =========================================================================
    # LOCALIZADORES (Mapeados según el comportamiento real del DOM de MUI)
    # =========================================================================
    
    # --- Vista Pública, Buscador y Solapas ---
    BOTON_CONSULTAR_INVENTARIO = (By.XPATH, "//button[contains(text(), 'Consultar inventario')]")
    TAB_EMPRESAS = (By.XPATH, "//*[contains(text(), 'Empresas')]")
    TAB_ATRACTIVOS = (By.XPATH, "//*[contains(text(), 'Atractivos')]")
    BUSCADOR_TEXTO = (By.XPATH, "//input[@id='search-input' or contains(@placeholder, 'Buscar')]")
    BOTON_BUSCAR = (By.CSS_SELECTOR, "button.search-button")
    
    # --- Modal de Filtros (Estructura de Comboboxes acotada al contenedor del Dialog) ---
    BOTON_ABRIR_FILTROS = (By.XPATH, "//button[contains(., 'Filtros')]")
    BOTON_APLICAR_FILTROS = (By.XPATH, "//button[contains(., 'Aplicar filtros') or contains(., 'Aplicar')]")
    
    # Contenedor genérico del modal/drawer flotante de Material-UI para delimitar las búsquedas
    MODAL_FILTROS = "//div[@role='dialog' or contains(@class, 'MuiDialog-') or contains(@class, 'MuiModal-') or contains(@class, 'MuiDrawer-')]"
    
    # Identificamos las cajas de los combos basándonos estrictamente en su orden dentro del Modal activo
    COMBO_DEPARTAMENTO = (By.XPATH, f"({MODAL_FILTROS}//div[@role='combobox'])[1]")
    COMBO_MUNICIPIO = (By.XPATH, f"({MODAL_FILTROS}//div[@role='combobox'])[2]")
    COMBO_DISTRITO = (By.XPATH, f"({MODAL_FILTROS}//div[@role='combobox'])[3]")
    
    # Localizador del contenedor principal del documento para lecturas globales de texto
    CUERPO_PAGINA = (By.TAG_NAME, "body")

    SELECT_REGION = (By.NAME, "region")
    
    # --- Acciones de Grilla / Home ---
    BOTON_REGISTRAR_EMPRESA = (By.XPATH, "//button[contains(text(), 'Agregar empresa') or contains(text(), 'Registrar empresa')]")
    
    # --- Formulario de Registro: 1) Personería ---
    RADIO_PERSONERIA_JURIDICA = (By.XPATH, "//input[@value='Jurídica']")
    RADIO_PERSONERIA_SAS = (By.XPATH, "//input[@value='SAS']")
    RADIO_PERSONERIA_NATURAL = (By.XPATH, "//input[@value='Natural']")
    
    # --- Formulario de Registro: 2) Información General ---
    TXT_NOMBRE_COMERCIAL = (By.NAME, "nombreComercial")
    TXT_ANIO_OPERACIONES = (By.NAME, "anioOperaciones")
    SELECT_TIPO_RECURSO = (By.NAME, "tipoRecurso")
    SELECT_TAMANIO_EMPRESA = (By.NAME, "tamanioEmpresa")
    TXT_IVA = (By.NAME, "registroContribuyente")
    SELECT_RUBRO_PRINCIPAL = (By.NAME, "rubroPrincipal")
    SELECT_CLASIFICACION_PRINCIPAL = (By.NAME, "clasificacionPrincipal")
    
    # --- Formulario de Registro: 3) Localización ---
    TXT_DIRECCION = (By.NAME, "direccion")
    SELECT_TIPO_UBICACION = (By.NAME, "tipoUbicacion")
    TXT_LATITUD = (By.NAME, "latitud")
    TXT_LONGITUD = (By.NAME, "longitud")
    SELECT_DESTINO_ESPECIFICO = (By.NAME, "destinoEspecifico")

    # --- Formulario de Registro: 6 & 7) Contacto y Atención ---
    TXT_WEB = (By.NAME, "paginaWeb")
    TXT_EMAIL_ATENCION = (By.NAME, "correoElectronico")
    TXT_TELEFONO_FIJO = (By.NAME, "telefonoFijo")
    TXT_CELULAR = (By.NAME, "celular")

    # --- Botones de Control del Formulario ---
    BOTON_GUARDAR_BORRADOR = (By.XPATH, "//button[contains(text(), 'Guardar')]")
    BOTON_CONFIRMAR_TRAMITE = (By.XPATH, "//button[contains(text(), 'Confirmar')]")

    # =========================================================================
    # MÉTODOS DE INTERACCIÓN (Acciones de negocio / Keywords)
    # =========================================================================

    def aplicar_busqueda_rapida(self, texto: str):
        """Ingresa el texto en el buscador principal para filtrado dinámico."""
        self.escribir(self.BUSCADOR_TEXTO, texto)

    def filtrar_con_filtros_avanzados(self, departamento=None, municipio=None, distrito=None, rubro=None, categoria=None, tipo=None, clasificacion=None):
        """Abre el modal, procesa los Chips jerárquicos primero y luego ejecuta los dropdowns de ubicación."""
        self.hacer_clic(self.BOTON_ABRIR_FILTROS)
        time.sleep(0.6)  # Sincronización para la apertura del modal animado
        
        # --- 1. SELECCIÓN DE CHIPS (Categorías, Tipos, Clasificaciones) ---
        # Usamos normalize-space y una estrategia doble de click para asegurar el cambio de estado en React
        if rubro:
            CHIP_RUBRO = (By.XPATH, f"//*[contains(@class, 'MuiChip-label') and (normalize-space()='{rubro}' or contains(normalize-space(), '{rubro}'))]")
            elemento_rubro = self.wait.until(EC.element_to_be_clickable(CHIP_RUBRO))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_rubro)
            time.sleep(0.2)
            try:
                elemento_rubro.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", elemento_rubro)
            time.sleep(0.4)

        if categoria:
            CHIP_CAT = (By.XPATH, f"//*[contains(@class, 'MuiChip-label') and (normalize-space()='{categoria}' or contains(normalize-space(), '{categoria}'))]")
            elemento_cat = self.wait.until(EC.element_to_be_clickable(CHIP_CAT))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_cat)
            time.sleep(0.2)
            try:
                elemento_cat.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", elemento_cat)
            time.sleep(0.4)

        if tipo:
            CHIP_TIPO = (By.XPATH, f"//*[contains(@class, 'MuiChip-label') and (normalize-space()='{tipo}' or contains(normalize-space(), '{tipo}'))]")
            elemento_tipo = self.wait.until(EC.element_to_be_clickable(CHIP_TIPO))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_tipo)
            time.sleep(0.2)
            try:
                elemento_tipo.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", elemento_tipo)
            time.sleep(0.4)
            
        if clasificacion:
            CHIP_CLASIFICACION = (By.XPATH, f"//*[contains(@class, 'MuiChip-label') and (normalize-space()='{clasificacion}' or contains(normalize-space(), '{clasificacion}'))]")
            elemento_clasi = self.wait.until(EC.element_to_be_clickable(CHIP_CLASIFICACION))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_clasi)
            time.sleep(0.2)
            try:
                elemento_clasi.click()
            except Exception:
                self.driver.execute_script("arguments[0].click();", elemento_clasi)
            time.sleep(0.4)

        # --- 2. SELECCIÓN DE DROPDOWNS (Ubicación Geográfica) ---
        # Forzamos scroll e interacción nativa (.click()) indispensable para activar el menú flotante en MUI
        if departamento:
            elemento_combo_depto = self.wait.until(EC.element_to_be_clickable(self.COMBO_DEPARTAMENTO))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_combo_depto)
            time.sleep(0.2)
            elemento_combo_depto.click()  
            time.sleep(0.5)
            
            # Ampliamos el Xpath de la opción para que soporte tanto 'li' como estructuras genéricas de Autocomplete/Select
            OPCION_DEPTO = (By.XPATH, f"//ul[@role='listbox']//*[self::li or @role='option'][normalize-space()='{departamento}' or contains(normalize-space(), '{departamento}')]")
            elemento_opcion_depto = self.wait.until(EC.element_to_be_clickable(OPCION_DEPTO))
            elemento_opcion_depto.click()
            time.sleep(1.2)  # Sincronización para la carga asincrónica de municipios

        if municipio:
            elemento_combo_muni = self.wait.until(EC.element_to_be_clickable(self.COMBO_MUNICIPIO))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_combo_muni)
            time.sleep(0.2)
            elemento_combo_muni.click()
            time.sleep(0.5)
            
            OPCION_MUNI = (By.XPATH, f"//ul[@role='listbox']//*[self::li or @role='option'][normalize-space()='{municipio}' or contains(normalize-space(), '{municipio}')]")
            elemento_opcion_muni = self.wait.until(EC.element_to_be_clickable(OPCION_MUNI))
            elemento_opcion_muni.click()
            time.sleep(1.2)  # Sincronización para la carga asincrónica de distritos
            
        if distrito:
            elemento_combo_dist = self.wait.until(EC.element_to_be_clickable(self.COMBO_DISTRITO))
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento_combo_dist)
            time.sleep(0.2)
            elemento_combo_dist.click()
            time.sleep(0.5)
            
            OPCION_DIST = (By.XPATH, f"//ul[@role='listbox']//*[self::li or @role='option'][normalize-space()='{distrito}' or contains(normalize-space(), '{distrito}')]")
            elemento_opcion_dist = self.wait.until(EC.element_to_be_clickable(OPCION_DIST))
            elemento_opcion_dist.click()
            time.sleep(0.5)
            
        self.hacer_clic(self.BOTON_APLICAR_FILTROS)

    def esperar_presencia_de_texto(self, texto_esperado: str, timeout=10) -> bool:
        """Detiene la prueba hasta que el texto del resultado aparezca en el DOM."""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(self.CUERPO_PAGINA, texto_esperado)
            )
            return True
        except Exception:
            return False

    def obtener_texto_resultados(self) -> str:
        """Captura el texto visible en toda la pantalla para las aserciones de contenido."""
        return self.driver.find_element(*self.CUERPO_PAGINA).text

    def iniciar_registro_empresa(self):
        self.hacer_clic(self.BOTON_REGISTRAR_EMPRESA)

    def completar_personeria(self, tipo: str):
        tipo_upper = tipo.upper()
        if "JURIDICA" in tipo_upper:
            self.hacer_clic(self.RADIO_PERSONERIA_JURIDICA)
        elif "SAS" in tipo_upper:
            self.hacer_clic(self.RADIO_PERSONERIA_SAS)
        else:
            self.hacer_clic(self.RADIO_PERSONERIA_NATURAL)

    def llenar_informacion_general(self, nombre: str, recurso: str, rubro: str, clasificacion: str, anio=""):
        self.escribir(self.TXT_NOMBRE_COMERCIAL, nombre)
        if anio:
            self.escribir(self.TXT_ANIO_OPERACIONES, anio)
        self.seleccionar_por_texto(self.SELECT_TIPO_RECURSO, recurso)
        self.seleccionar_por_texto(self.SELECT_RUBRO_PRINCIPAL, rubro)
        self.seleccionar_por_texto(self.SELECT_CLASIFICACION_PRINCIPAL, clasificacion)

    def llenar_localizacion(self, direccion: str, tipo_ubicacion: str, destino_especifico: str):
        self.escribir(self.TXT_DIRECCION, direccion)
        self.seleccionar_por_texto(self.SELECT_TIPO_UBICACION, tipo_ubicacion)
        self.seleccionar_por_texto(self.SELECT_DESTINO_ESPECIFICO, destino_especifico)

    def guardar_borrador(self):
        self.hacer_clic(self.BOTON_GUARDAR_BORRADOR)

    def enviar_a_revision(self):
        self.hacer_clic(self.BOTON_CONFIRMAR_TRAMITE)