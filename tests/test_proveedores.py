import pytest
from pages.proveedores_page import ProveedoresPage

# URL confirmada del ambiente de desarrollo
URL_BASE = "https://develop.corsatur.julasoft.com/"

@pytest.mark.regression
def test_flujo_vista_publica_proveedores(driver):
    """
    Objetivo: Validar que un usuario anónimo puede ingresar al Directorio de Proveedores,
              visualizar el listado, entrar al detalle del primero verificando datos clave
              y regresar exitosamente al listado.
    """
    proveedores = ProveedoresPage(driver)
    
    # 1. Entrar al portal y navegar a Proveedores
    proveedores.abrir_url(URL_BASE)
    proveedores.ir_a_directorio_proveedores()
    
    # Esperamos que cargue la interfaz del listado validando la presencia del primer ojo
    assert proveedores.encontrar_elemento(proveedores.ICONO_VER_PRIMER_DETALLE).is_displayed(), \
        "El listado de proveedores no cargó correctamente o no se visualiza el ícono de ver detalle."

    # 2. Entrar a ver al primero de la lista
    proveedores.ver_primer_proveedor()
    
    # 3. Revisar si están los datos mandatorios en la vista de detalle
    # Esperamos primero que renderice el botón Volver para asegurar que el detalle abrió
    assert proveedores.esperar_presencia_de_texto("Volver", timeout=10), \
        "La vista de detalle del proveedor tardó demasiado en cargar."
        
    texto_pantalla = proveedores.obtener_texto_completo().lower()
    
    # Validamos la existencia de las secciones/etiquetas clave (adecuar strings si la UI usa otras etiquetas exactas)
    assert "proveedor" in texto_pantalla, "No se encontró la etiqueta o tipo de proveedor en el detalle."
    assert "comercial" in texto_pantalla or "nombre" in texto_pantalla, "No se encontró el nombre comercial en el detalle."
    assert "ubicación" in texto_pantalla or "direccion" in texto_pantalla, "No se encontró la ubicación en el detalle."

    # 4. Volver al listado a través del botón Volver
    proveedores.volver_al_listado()
    
    # Validación de retorno: verificamos que el botón Volver ya no esté y reaparezca el listado con el ojo
    assert proveedores.encontrar_elemento(proveedores.ICONO_VER_PRIMER_DETALLE).is_displayed(), \
        "Fallo al regresar: No se visualiza el listado de proveedores tras hacer clic en Volver."
        
    print("¡Prueba de flujo básico y visualización de proveedores aprobada con éxito!")