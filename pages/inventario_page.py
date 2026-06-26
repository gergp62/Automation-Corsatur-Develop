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
    # LOCALIZADORES (Mapeados según el documento de requerimientos SIIT_CU002)
    # =========================================================================
    
    # --- Vista Pública, Buscador y Solapas ---
    BOTON_CONSULTAR_INVENTARIO = (By.XPATH, "//button[contains(text(), 'Consultar inventario')]")
    TAB_EMPRESAS = (By.XPATH, "//*[contains(text(), 'Empresas')]")
    TAB_ATRACTIVOS = (By.XPATH, "//*[contains(text(), 'Atractivos')]")
    BUSCADOR_TEXTO = (By.XPATH, "//input[@id='search-input' or contains(@placeholder, 'Buscar')]")
    BOTON_BUSCAR = (By.CSS_SELECTOR, "button.search-button")
    
    # --- Modal de Filtros (Estructura Mixta Material-UI de HU001) ---
    BOTON_ABRIR_FILTROS = (By.XPATH, "//button[contains(., 'Filtros')]")
    BOTON_APLICAR_FILTROS = (By.XPATH, "//button[contains(., 'Aplicar filtros') or contains(., 'Aplicar')]")
    
    # Selectores del Modal - Tipo Dropdown (Párrafos)
    COMBO_DEPARTAMENTO = (By.XPATH, "//p[contains(text(), 'Seleccionar departamento')]")
    COMBO_MUNICIPIO = (By.XPATH, "//p[contains(text(), 'Seleccionar municipio')]")
    COMBO_DISTRITO = (By.XPATH, "//p[contains(text(), 'Seleccionar distrito')]")
    
    # Localizador del contenedor principal del documento para lecturas globales de texto
    CUERPO_PAGINA = (By.TAG_NAME, "body")

    SELECT_REGION = (By.NAME, "region")
    
    # --- Acciones de Grilla / Home ---
    BOTON_REGISTRAR_EMPRESA = (By.XPATH, "//button[contains(text(), 'Agregar empresa') or contains(text(), 'Registrar empresa')]")
    
    # Captura el primer botón de Material-UI que contenga exactamente el texto "Ver"
    BOTON_VER_DETALLE_PRIMERO = (By.XPATH, "(//button[contains(@class, 'MuiButton-root') and contains(text(), 'Ver')])[1]")
    
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

    def filtrar_con_filtros_avanzados(self, departamento=None, municipio=None, distrito=None, rubro=None, clasificacion=None):
        """Abre el modal de filtros y combina dropdowns y chips seleccionables."""
        self.hacer_clic(self.BOTON_ABRIR_FILTROS)
        
        if departamento:
            self.hacer_clic(self.COMBO_DEPARTAMENTO)
            OPCION_DEPTO = (By.XPATH, f"//li[contains(text(), '{departamento}') or contains(., '{departamento}')]")
            self.hacer_clic(OPCION_DEPTO)

        if municipio:
            self.hacer_clic(self.COMBO_MUNICIPIO)
            OPCION_MUNI = (By.XPATH, f"//li[contains(text(), '{municipio}') or contains(., '{municipio}')]")
            self.hacer_clic(OPCION_MUNI)
            
        if distrito:
            self.hacer_clic(self.COMBO_DISTRITO)
            OPCION_DIST = (By.XPATH, f"//li[contains(text(), '{distrito}') or contains(., '{distrito}')]")
            self.hacer_clic(OPCION_DIST)
            
        if rubro:
            CHIP_RUBRO = (By.XPATH, f"//span[contains(@class, 'MuiChip-label') and text()='{rubro}']")
            self.hacer_clic(CHIP_RUBRO)
            
        if clasificacion:
            CHIP_CLASIFICACION = (By.XPATH, f"//span[contains(@class, 'MuiChip-label') and text()='{clasificacion}']")
            self.hacer_clic(CHIP_CLASIFICACION)
            
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

    def ver_primer_detalle(self):
        """Hace clic en el botón o ícono de 'Ver detalle' del primer registro del listado."""
        self.hacer_clic(self.BOTON_VER_DETALLE_PRIMERO)

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