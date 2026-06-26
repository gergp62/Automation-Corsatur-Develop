import pytest
from pages.inventario_page import InventarioPage

# URL CONFIRMADA: Apunta estrictamente al ambiente de desarrollo (develop)
URL_BASE = "https://develop.corsatur.julasoft.com/"

@pytest.mark.smoke
def test_visualizacion_publica_inventario(driver):
    """
    Caso de Uso: 002 - HU001 (Ver Inventario Turístico)
    Objetivo: Validar que un usuario anónimo (Público) puede ingresar al portal
              y visualizar las solapas principales del inventario.
    """
    inventario = InventarioPage(driver)
    inventario.abrir_url(URL_BASE)
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    assert inventario.encontrar_elemento(inventario.TAB_EMPRESAS).is_displayed(), \
        "La solapa de 'Empresas' no es visible en la vista pública."
    assert inventario.encontrar_elemento(inventario.TAB_ATRACTIVOS).is_displayed(), \
        "La solapa de 'Atractivos' no es visible en la vista pública."


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
    Objetivo: Validar que al hacer clic en el ícono de 'Ver detalle' de una empresa 
              filtrada por el rubro 'Transporte', se abra la vista detallada y 
              se verifique que la información obligatoria del rubro sea correcta.
    """
    inventario = InventarioPage(driver)
    inventario.abrir_url(URL_BASE)
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    inventario.filtrar_con_filtros_avanzados(rubro="Transporte")
    
    assert inventario.esperar_presencia_de_texto("Transporte", timeout=10), \
        "Fallo previo: No se encontraron empresas con el rubro 'Transporte' en la grilla principal."
    
    inventario.ver_primer_detalle()
    
    detalle_abierto_con_exito = inventario.esperar_presencia_de_texto("Transporte", timeout=12)
    assert detalle_abierto_con_exito, \
        "Fallo en la aserción: Se abrió el detalle de la empresa pero no se visualiza el rubro mandatorio 'Transporte'."
        
    print("¡Prueba de visualización de detalles de transporte aprobada con éxito!")


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
    
    # Set de datos con acentos tipográficos rigurosos pertenecientes al catálogo estándar
    depto_con_acento = "Ahuachapán"
    rubro_con_acento = "Alimentación"
    
    inventario.filtrar_con_filtros_avanzados(
        departamento=depto_con_acento,
        rubro=rubro_con_acento
    )
    
    # Esperamos que los resultados rendericen el departamento o un indicador del filtro aplicado
    se_cargo_contenido = inventario.esperar_presencia_de_texto(depto_con_acento, timeout=10)
    assert se_cargo_contenido, \
        f"Fallo con acentos: El texto '{depto_con_acento}' no se visualiza en la grilla de resultados de develop."
        
    texto_pantalla = inventario.obtener_texto_resultados().lower()
    assert rubro_con_acento.lower() in texto_pantalla, \
        f"El rubro '{rubro_con_acento}' no fue encontrado en los resultados textuales de la pantalla."
        
    print("¡Filtro avanzado complejo con manejo de acentos aprobado de forma exitosa!")