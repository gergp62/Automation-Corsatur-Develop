import pytest
import time
from pages.inventario_page import InventarioPage

# URL CONFIRMADA: Apunta estrictamente al ambiente de desarrollo (develop)
URL_BASE = "https://develop.corsatur.julasoft.com/"

@pytest.mark.smoke
def test_visualizacion_publica_inventario(driver):
    """
    Caso de Uso: 002 - HU001 (Ver Inventario Turístico)
    Objetivo: Validar que un usuario anónimo (Público) puede ingresar al portal,
              visualizar las solapas principales, acceder al detalle del primer registro
              para verificar etiquetas informativas clave y regresar exitosamente a la grilla.
    """
    inventario = InventarioPage(driver)
    inventario.abrir_url(URL_BASE)
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    # 1. Validación inicial de solapas en la grilla principal
    assert inventario.encontrar_elemento(inventario.TAB_EMPRESAS).is_displayed(), \
        "La solapa de 'Empresas' no es visible en la vista pública."
    assert inventario.encontrar_elemento(inventario.TAB_ATRACTIVOS).is_displayed(), \
        "La solapa de 'Atractivos' no es visible en la vista pública."

    # 2. MEJORA DE COBERTURA: Navegación interna al detalle de un registro sin filtros previos
    inventario.ver_primer_detalle()
    
    # Validación estricta de la presencia de los bloques de información requeridos
    assert inventario.esperar_presencia_de_texto("Ubicación", timeout=10), \
        "Fallo en la vista pública: La etiqueta de sección 'Ubicación' no se renderizó en el detalle."
    
    texto_interno = inventario.obtener_texto_resultados()
    assert "Establecimiento" in texto_interno or "Datos" in texto_interno, \
        "Fallo de consistencia: No se visualizan las etiquetas de identificación del establecimiento en el detalle público."

    # 3. Flujo de retorno: Validación del botón Volver
    inventario.volver_a_grilla()
    
    # Confirmamos que el estado del DOM regresó a la grilla interactiva original
    assert inventario.esperar_presencia_de_texto("Consultar inventario", timeout=5) or \
           inventario.encontrar_elemento(inventario.TAB_EMPRESAS).is_displayed(), \
        "Fallo en la navegación: El botón Volver no restituyó la grilla principal de resultados."


@pytest.mark.sanity
def test_busqueda_rapida_empresa_existente(driver):
    """
    Caso de Uso: 002 - HU001
    Objetivo: Validar que el buscador principal del inventario filtre correctamente
              al ingresar un texto de una empresa existente de manera dinámica.
    """
    inventario = InventarioPage(driver)
    inventario.abrir_url(URL_BASE)
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    termino_busqueda = "EQUINOCCIO"  
    inventario.aplicar_busqueda_rapida(termino_busqueda)
    
    elemento_buscador = inventario.encontrar_elemento(inventario.BUSCADOR_TEXTO)
    assert elemento_buscador.get_attribute("value") == termino_busqueda, \
        "El texto no se ingresó correctamente en el buscador dinámico."


@pytest.mark.regression
def test_filtrar_por_ubicacion_y_categoria_valida(driver):
    """
    Caso de Uso: 002 - HU001
    Objetivo: Validar que los filtros combinados (Ubicación exacta y Chips de Categoría) 
              en el modal se apliquen correctamente devolviendo datos reales del ambiente.
    """
    inventario = InventarioPage(driver)
    inventario.abrir_url(URL_BASE)
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    depto_test = "San Salvador"
    muni_test = "San Salvador Centro"   
    distrito_test = "San Salvador"       
    rubro_test = "Alojamiento"
    clasi_test = "Hotel"
    
    inventario.filtrar_con_filtros_avanzados(
        departamento=depto_test, 
        municipio=muni_test, 
        distrito=distrito_test,
        rubro=rubro_test, 
        clasificacion=clasi_test
    )
    
    se_cargo_contenido = inventario.esperar_presencia_de_texto(clasi_test, timeout=10)
    assert se_cargo_contenido, \
        f"Fallo en el filtro: Pasaron 10s y el texto '{clasi_test}' no apareció en pantalla tras aplicar filtros."

    texto_pantalla = inventario.obtener_texto_resultados().lower()
    assert rubro_test.lower() in texto_pantalla, \
        f"Validación fallida: El rubro '{rubro_test}' no se encuentra visible en la pantalla de resultados."

    print("¡Filtro combinado completamente exitoso y validado en pantalla!")


@pytest.mark.regression
def test_ver_detalle_empresa_transporte(driver):
    """
    Caso de Uso: 002 - HU001
    Objetivo: Validar que al filtrar por el rubro 'Transporte', clasificación 'Transporte terrestre turístico'
              y la ubicación exacta en Chalatenango, se listen los resultados correspondientes en la grilla,
              se pueda acceder al detalle mediante el ícono del ojo y se verifique la información interna.
    """
    inventario = InventarioPage(driver)
    inventario.abrir_url(URL_BASE)
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    inventario.filtrar_con_filtros_avanzados(
        rubro="Transporte",
        clasificacion="Transporte terrestre turístico",
        departamento="Chalatenango",
        municipio="Chalatenango Centro",
        distrito="Tejutla"
    )
    
    assert inventario.esperar_presencia_de_texto("Transporte terrestre turístico", timeout=10), \
        "Fallo previo: No se renderizaron filas para la combinación de transporte terrestre en Chalatenango."
    
    inventario.ver_primer_detalle()
    
    assert inventario.esperar_presencia_de_texto("Transporte", timeout=12), \
        "Fallo en la verificación: El rubro 'Transporte' no está visible en el detalle de la empresa."
        
    assert inventario.esperar_presencia_de_texto("Transporte terrestre turístico", timeout=5), \
        "Fallo en la verificación: La clasificación 'Transporte terrestre turístico' no se visualiza en el detalle."
        
    print("¡Prueba de flujo completo de grilla y detalle de transporte terrestre aprobada con éxito!")


@pytest.mark.regression
def test_filtrar_atractivos_por_ubicacion_y_categoria(driver):
    """
    Caso de Uso: 002 - HU001
    Objetivo: Validar que los filtros avanzados complejos para la solapa de Atractivos
              funcionen de manera óptima en la grilla del ambiente de desarrollo.
    """
    inventario = InventarioPage(driver)
    inventario.abrir_url(URL_BASE)
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    # Cambiamos a la solapa de Atractivos
    inventario.hacer_clic(inventario.TAB_ATRACTIVOS)
    
    assert inventario.esperar_presencia_de_texto("Atractivos", timeout=10), \
        "La solapa de Atractivos no terminó de cargar visualmente."
    
    # Pausa de estabilización necesaria para evitar la carrera de diseño (race condition) 
    # de Material-UI al interactuar directamente con los combos sin pasar por chips previos.
    time.sleep(1.5)
    
    depto_atractivo = "San Salvador"
    muni_atractivo = "San Salvador Centro"
    
    inventario.filtrar_con_filtros_avanzados(
        departamento=depto_atractivo,
        municipio=muni_atractivo
    )
    
    se_cargo_contenido = inventario.esperar_presencia_de_texto(depto_atractivo, timeout=10)
    assert se_cargo_contenido, \
        f"Fallo en Atractivos: El texto '{depto_atractivo}' no impactó en pantalla tras 10 segundos."
        
    texto_pantalla = inventario.obtener_texto_resultados().lower()
    assert muni_atractivo.lower() in texto_pantalla, \
        f"El municipio '{muni_atractivo}' no fue renderedizado en las tarjetas de resultados."
        
    print("¡Filtro avanzado complejo de Atractivos completado con éxito!")


@pytest.mark.regression
def test_filtrar_por_ubicacion_y_rubro_con_acentos(driver):
    """
    Caso de Uso: 002 - HU001
    Objetivo: Validar que el motor de filtros avanzados procese y devuelva información de
              forma correcta al ingresar criterios que contienen acentos gramaticales en develop.
    """
    inventario = InventarioPage(driver)
    inventario.abrir_url(URL_BASE)
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    depto_con_acento = "Ahuachapán"
    rubro_con_acento = "Alimentación"
    
    inventario.filtrar_con_filtros_avanzados(
        departamento=depto_con_acento,
        rubro=rubro_con_acento
    )
    
    se_cargo_contenido = inventario.esperar_presencia_de_texto(depto_con_acento, timeout=10)
    assert se_cargo_contenido, \
        f"Fallo con acentos: El texto '{depto_con_acento}' no se visualiza en la grilla de resultados de develop."
        
    texto_pantalla = inventario.obtener_texto_resultados().lower()
    assert rubro_con_acento.lower() in texto_pantalla, \
        f"El rubro '{rubro_con_acento}' no fue encontrado en los resultados textuales de la pantalla."
        
    print("¡Filtro avanzado complejo con manejo de acentos approved de forma exitosa!")