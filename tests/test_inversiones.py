import pytest
import time
from pages.inversiones_page import InversionesPage

URL_BASE = "https://develop.corsatur.julasoft.com/"

@pytest.mark.regression
def test_flujo_vista_publica_inversiones(driver):
    """
    Test: Validar acceso al módulo de Inversiones en 'develop', verificar redirección 
          externa segura abriendo una nueva pestaña y retorno limpio a la Home Page.
    """
    inversiones = InversionesPage(driver)
    inversiones.abrir_url(URL_BASE)
    
    # 1. Ingresar a la sección de Inversiones desde la Home de Develop
    inversiones.ir_a_vista_inversiones()
    
    # Validar que cargó el texto y el botón clave en la vista de inversiones
    assert inversiones.esperar_presencia_de_texto("Invertir en El Salvador", timeout=12), \
        "No se renderizó el botón o el contenido del módulo de Inversiones."

    # Guardar identificador de la pestaña original (Corsatur)
    pestaña_original = driver.current_window_handle

    # 2. Hacer clic para disparar la apertura de la ventana de gobierno externa
    inversiones.hacer_clic_invertir_en_salvador()

    todas_las_pestañas = driver.window_handles
    assert len(todas_las_pestañas) > 1, "La acción no abrió una nueva pestaña de navegación."

    # 3. Intercambiar el foco del driver hacia la nueva pestaña
    for pestaña in todas_las_pestañas:
        if pestaña != pestaña_original:
            driver.switch_to.window(pestaña)
            break

    # Validar el dominio gubernamental externo
    url_esperada_gob = "https://investinelsalvador.gob.sv/"
    url_actual = driver.current_url
    print(f"\n[DEBUG QA] -> Ventana externa apuntando a: {url_actual}")
    
    assert url_esperada_gob in url_actual, \
        f"URL externa incorrecta. Se obtuvo '{url_actual}' pero se esperaba '{url_esperada_gob}'."

    # Limpieza: Cerrar el sitio de gobierno y restablecer el foco en nuestro portal original
    driver.close()
    driver.switch_to.window(pestaña_original)
    time.sleep(1.0)

    # 4. Clic en Volver para que nos devuelva al inicio
    inversiones.volver_a_la_home()
    
    # Verificación final utilizando el título principal de la sección para blindar la aserción
    assert inversiones.esperar_presencia_de_texto("Desarrollo e inversión", timeout=15), \
        "El botón 'Volver' no redirigió correctamente al usuario a la Home de la aplicación o la página tardó en cargar."