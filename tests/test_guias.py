import pytest
import time
from pages.guias_page import GuiasPage

# URL Base apuntando de forma estricta al entorno bajo pruebas
URL_BASE = "https://develop.corsatur.julasoft.com/"

@pytest.mark.regression
def test_busqueda_directa_guia(driver):
    """
    Test 1: Validar la búsqueda directa de guías ingresando estrictamente por el botón 'Ver guías'.
    """
    guias = GuiasPage(driver)
    guias.abrir_url(URL_BASE)

    print("\n[PASO] Navegando al listado de Guías Turísticos desde la interfaz principal...")
    guias.ir_a_vista_guias()

    print("[PASO] Ejecutando búsqueda por término 'German'...")
    guias.buscar_en_barra("German")

    assert guias.verificar_grilla_con_datos(), "La búsqueda directa no devolvió resultados en la grilla o el selector falló."
    print("¡Test 1 superado de manera exitosa!")


@pytest.mark.regression
def test_filtros_y_detalle_guia(driver):
    """
    Test 2: Validación de selectores de modalidad (Nacional, Zona, Independiente) accediendo por UI.
    """
    guias = GuiasPage(driver)
    guias.abrir_url(URL_BASE)

    print("\n[PASO] Navegando al listado de Guías Turísticos desde la interfaz principal...")
    guias.ir_a_vista_guias()

    print("[PASO] Abriendo panel lateral de filtros...")
    guias.abrir_panel_filtros()

    print("[PASO] Seleccionando valores en el bloque 'Modalidad y Tipo'...")
    guias.seleccionar_opcion_dropdown("modalidad", "Nacional")
    guias.seleccionar_opcion_dropdown("zona", "paracentral")
    guias.seleccionar_opcion_dropdown("independiente", "Independiente")

    print("[PASO] Aplicando filtros configurados...")
    guias.aplicar_filtros()

    print("[DEBUG VISUAL] Esperando 5 segundos para observar la grilla filtrada en pantalla...")
    time.sleep(5.0)

    print("[LOG QA] -> Test 2: Validación de selectores de modalidad finalizada.")


@pytest.mark.regression
def test_filtros_geograficos_avanzados(driver):
    """
    Test 3: Validar comportamiento dinámico de los selectores geográficos en cascada (Región / Departamento).
    """
    guias = GuiasPage(driver)
    guias.abrir_url(URL_BASE)

    print("\n[PASO] Navegando al listado de Guías Turísticos desde la interfaz principal...")
    guias.ir_a_vista_guias()

    print("[PASO] Abriendo panel lateral de filtros...")
    guias.abrir_panel_filtros()

    print("[PASO] Seleccionando valores geográficos (Región / Departamento)...")
    guias.seleccionar_opcion_dropdown("región", "Central")
    guias.seleccionar_opcion_dropdown("departamento", "San Salvador")

    print("[PASO] Aplicando filtros configurados...")
    guias.aplicar_filtros()

    assert guias.verificar_grilla_con_datos(), "El filtro geográfico en cascada no arrojó resultados en la grilla."
    print("¡Test 3 superado con éxito!")