import pytest
import time
from pages.proveedores_page import ProveedoresPage

URL_BASE = "https://develop.corsatur.julasoft.com/"

@pytest.mark.regression
def test_flujo_vista_publica_proveedores(driver):
    """
    Test 1: Validar acceso al Directorio de Proveedores, verificar la grilla,
            ingresar al primer resultado, auditar datos obligatorios y retornar limpiamente.
    """
    proveedores = ProveedoresPage(driver)
    proveedores.abrir_url(URL_BASE)
    proveedores.ir_a_directorio_proveedores()
    
    # 1. Verificar visualización del botón del ojo e ingresar al primer resultado
    assert proveedores.encontrar_elemento(proveedores.ICONO_VER_PRIMER_DETALLE).is_displayed(), \
        "La interfaz del listado público no renderizó los botones de acción del detalle."
    proveedores.ver_primer_proveedor()
    
    # 2. Auditar datos mandatorios en la vista interna de detalle
    assert proveedores.esperar_presencia_de_texto("Volver", timeout=10), \
        "La vista detallada del proveedor no cargó o el botón 'Volver' no se encuentra visible."
    
    texto_pantalla = proveedores.obtener_texto_completo().lower()
    assert "proveedor" in texto_pantalla, "Falta la etiqueta identificatoria o tipo de proveedor en el detalle."
    assert "comercial" in texto_pantalla or "nombre" in texto_pantalla, "El nombre comercial/razón social no figura en pantalla."
    assert "ubicación" in texto_pantalla or "direccion" in texto_pantalla, "La información geográfica de ubicación está ausente."

    # 3. Regresar al listado general
    proveedores.volver_al_listado()
    assert proveedores.encontrar_elemento(proveedores.ICONO_VER_PRIMER_DETALLE).is_displayed(), \
        "Error al retornar: No se volvió a renderizar el listado general con sus botones de acciones."


@pytest.mark.sanity
def test_filtrar_proveedores_por_busqueda_texto(driver):
    """
    Test 2: Validar la búsqueda directa por barra ("AYL"), ingresar
            al resultado filtrado en la grilla y validar consistencia del negocio.
    """
    proveedores = ProveedoresPage(driver)
    proveedores.abrir_url(URL_BASE)
    proveedores.ir_a_directorio_proveedores()
    
    # 1. Ingresar el texto en la barra de búsqueda (el filtrado es reactivo y asíncrono)
    texto_busqueda = "AYL"
    proveedores.buscar_en_barra(texto_busqueda)
    
    # 2. Hacer clic en el ojo del primer resultado filtrado
    proveedores.ver_primer_proveedor()
    
    # 3. Verificar consistencia dentro del detalle y regresar
    assert proveedores.esperar_presencia_de_texto("Volver", timeout=10), \
        "El detalle del proveedor filtrado por texto tardó demasiado en renderizar."
    
    texto_detalle = proveedores.obtener_texto_completo().lower()
    assert texto_busqueda.lower() in texto_detalle, \
        f"Inconsistencia: El término buscado '{texto_busqueda}' no coincide con los datos del detalle cargado."
        
    proveedores.volver_al_listado()


@pytest.mark.regression
def test_filtrar_proveedores_avanzado_completo(driver):
    """
    Test 3: Validar parametrización completa de filtros geográficos (5 niveles) + Tipo de proveedor.
            Acceder al resultado devuelto, auditar consistencia de datos cruzados y volver.
    """
    proveedores = ProveedoresPage(driver)
    proveedores.abrir_url(URL_BASE)
    proveedores.ir_a_directorio_proveedores()
    
    # Data de prueba validada para el ambiente de desarrollo
    pais_test = "El Salvador"
    region_test = "Zona occidental"
    depto_test = "Santa Ana"
    muni_test = "Santa Ana Centro"
    distrito_test = "Santa Ana"
    tipo_proveedor_test = "Distribuidores de vehículos"
    
    # 1. Aplicar la configuración completa en el modal
    proveedores.filtrar_proveedores_avanzado(
        pais=pais_test,
        region=region_test,
        departamento=depto_test,
        municipio=muni_test,
        distrito=distrito_test,
        tipo_proveedor=tipo_proveedor_test
    )
    
    # 2. Entrar al detalle del primer resultado obtenido tras la aplicación del filtro
    proveedores.ver_primer_proveedor()
    
    # 3. Auditoría estricta de consistencia de negocio dentro del detalle
    assert proveedores.esperar_presencia_de_texto("Volver", timeout=12), \
        "La pantalla de detalle del proveedor seleccionado no se desplegó en el tiempo estipulado."
        
    texto_detalle = proveedores.obtener_texto_completo().lower()
    
    assert tipo_proveedor_test.lower() in texto_detalle, \
        f"Inconsistencia: El tipo de proveedor '{tipo_proveedor_test}' no se encuentra reflejado en el detalle."
    assert depto_test.lower() in texto_detalle, \
        f"Inconsistencia: El departamento de origen '{depto_test}' no coincide en la vista detallada."
    assert distrito_test.lower() in texto_detalle, \
        f"Inconsistencia: El distrito de origen '{distrito_test}' no figura en el cuerpo de datos del detalle."
        
    # 4. Cierre del ciclo regresando al listado principal
    proveedores.volver_al_listado()
    assert proveedores.encontrar_elemento(proveedores.BOTON_ABRIR_FILTROS).is_displayed(), \
        "Fallo crítico al regresar: El panel de control principal o la grilla quedaron inaccesibles."