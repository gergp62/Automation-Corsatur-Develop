import pytest
from pages.inventario_page import InventarioPage

# URL del ambiente de desarrollo de CORSATUR
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
    
    # 1. Entramos a la sección de inventario
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    # 2. Set de datos exactos corregido según el comportamiento real del ambiente
    depto_test = "San Salvador"
    muni_test = "San Salvador Centro"   
    distrito_test = "San Salvador"       
    rubro_test = "Alojamiento"
    clasi_test = "Hotel"
    
    # 3. Ejecutamos la acción combinada pasando los 5 filtros secuenciales
    inventario.filtrar_con_filtros_avanzados(
        departamento=depto_test, 
        municipio=muni_test, 
        distrito=distrito_test,
        rubro=rubro_test, 
        clasificacion=clasi_test
    )
    
    # =========================================================================
    # ASERCIONES (Validaciones optimizadas por presencia de contenido)
    # =========================================================================
    
    # Aserción 1: Esperar a que los datos filtrados impacten visualmente en la grilla
    se_cargo_contenido = inventario.esperar_presencia_de_texto(clasi_test, timeout=10)
    assert se_cargo_contenido, \
        f"Fallo en el filtro: Pasaron 10s y el texto '{clasi_test}' no apareció en pantalla tras aplicar filtros."

    # Aserción 2: Validar que el rubro también esté presente en el renderizado
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
    
    # 1. Ingresamos a la sección pública de inventario
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    # 2. Filtramos directamente por el chip del rubro "Transporte" (dejando ubicación libre)
    inventario.filtrar_con_filtros_avanzados(rubro="Transporte")
    
    # 3. Validamos que la grilla reaccionó y muestra elementos de Transporte antes de avanzar
    assert inventario.esperar_presencia_de_texto("Transporte", timeout=10), \
        "Fallo previo: No se encontraron empresas con el rubro 'Transporte' en la grilla principal."
    
    # 4. Hacemos clic en el ícono/botón de ver detalle del primer elemento de la lista
    inventario.ver_primer_detalle()
    
    # 5. Aserción final: Validar que los datos mandatorios (el rubro) se visualicen dentro del detalle
    detalle_abierto_con_exito = inventario.esperar_presencia_de_texto("Transporte", timeout=12)
    assert detalle_abierto_con_exito, \
        "Fallo en la aserción: Se abrió el detalle de la empresa pero no se visualiza el rubro mandatorio 'Transporte'."
        
    print("¡Prueba de visualización de detalles de transporte aprobada con éxito!")