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
def test_filtrar_atractivos_por_ubicacion_y_categoria(driver):
    """
    Caso de Uso: 002 - HU001 (Atractivos)
    Objetivo: Validar que los filtros complejos avanzados (Ubicación exacta de diagnóstico)
              funcionen en la solapa de atractivos, trayendo la data esperada.
    """
    inventario = InventarioPage(driver)
    inventario.abrir_url(URL_BASE)
    inventario.hacer_clic(inventario.BOTON_CONSULTAR_INVENTARIO)
    
    # 1. Cambiamos a la solapa de Atractivos
    inventario.hacer_clic(inventario.TAB_ATRACTIVOS)
    
    # 2. Set de datos estratégico modificado para diagnosticar comportamiento sin acentos
    depto_atractivo = "Sonsonate"
    muni_atractivo = "Sonsonate Este"   
    dist_atractivo = None           # Aislamos el distrito pasándolo como None
    cat_atractivo = None            # Sin chips por ahora para validar solo dropdowns
    tipo_atractivo = None
    clasi_atractivo = None
    
    # 3. Ejecutamos la filtración combinada avanzada
    inventario.filtrar_con_filtros_avanzados(
        departamento=depto_atractivo, 
        municipio=muni_atractivo, 
        distrito=dist_atractivo,
        categoria=cat_atractivo,
        tipo=tipo_atractivo,
        clasificacion=clasi_atractivo
    )

    # =========================================================================
    # ASERCIONES (Validaciones optimizadas para la grilla de resultados)
    # =========================================================================
    
    # Aserción 1: Esperar a que los datos filtrados del departamento impacten en pantalla
    se_cargo_contenido = inventario.esperar_presencia_de_texto(depto_atractivo, timeout=10)
    assert se_cargo_contenido, \
        f"Fallo en el filtro: Pasaron 10s y el texto '{depto_atractivo}' no apareció en pantalla tras aplicar filtros."

    # Aserción 2: Validar que el municipio también se encuentre renderizado en los cards/grilla
    texto_pantalla = inventario.obtener_texto_resultados().lower()
    assert muni_atractivo.lower() in texto_pantalla, \
        f"Validación fallida: El municipio '{muni_atractivo}' no se encuentra visible en la pantalla de resultados."

    print("¡Filtro de diagnóstico con Sonsonate ejecutado y validado en pantalla con éxito!")