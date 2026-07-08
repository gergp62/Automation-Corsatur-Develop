import pytest
from pages.pitn_page import PitnPage

URL_BASE = "https://develop.corsatur.julasoft.com/"

@pytest.mark.regression
def test_flujo_busquedas_y_filtros_pitn(driver):
    """
    Test: Validar el comportamiento de la grilla de Proyectos PITN utilizando
          búsqueda directa por texto, combinación de filtros laterales y control de nulos.
    """
    pitn = PitnPage(driver)
    pitn.abrir_url(URL_BASE)

    # 1. Acceder al módulo PITN desde la Home principal
    pitn.ir_a_vista_pitn()

    assert pitn.esperar_presencia_de_texto("Proyectos de interés turístico (PITN)", timeout=12), \
        "No se visualiza la cabecera correcta del módulo PITN."

    # 2. Búsqueda por texto con resultados ("Coconut")
    print("\n[PASO] Ejecutando búsqueda por término 'Coconut'...")
    pitn.buscar_en_barra("Coconut")

    assert pitn.esperar_presencia_de_texto("Coconut", timeout=10), \
        "La búsqueda por el término 'Coconut' no arrojó coincidencias en la grilla."

    # 3. Limpiar campo de búsqueda para restablecer la grilla
    print("[PASO] Limpiando barra de búsqueda...")
    pitn.buscar_en_barra("")

    # 4. Uso del panel de filtros laterales
    print("[PASO] Abriendo panel lateral y aplicando filtros por etiquetas...")
    pitn.abrir_panel_filtros()

    # Seleccionar las opciones tipo chip con textos exactos
    pitn.seleccionar_chip_filtro("Alojamiento")
    pitn.seleccionar_chip_filtro("Proyecto Nuevo")

    # Al aplicar los filtros, la UI actualiza y procesa la grilla
    pitn.aplicar_filtros_laterales()

    # Validación de datos cargados en grilla por los filtros
    assert pitn.verificar_grilla_con_datos(), \
        "Los filtros combinados no cargaron registros válidos en la grilla de resultados."

    # 5. Búsqueda directa por texto sin resultados ("sinresultado")
    print("[PASO] Ejecutando búsqueda directa controlada sin resultados...")
    pitn.buscar_en_barra("sinresultado")
    
    # Validación exacta pedida mapeando el mensaje del portal en minúsculas
    assert pitn.esperar_presencia_de_texto("No hay proyectos registrados", timeout=10), \
        "No se visualizó el mensaje esperado 'No hay proyectos registrados' al buscar un término inexistente."
        
    print("[LOG QA] -> ¡Flujo PITN completado exitosamente con normalización de texto!")