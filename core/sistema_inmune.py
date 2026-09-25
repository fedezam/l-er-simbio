# A_adir esta funci_n a tu archivo sistema_inmune.py existente

class AnalisisSeguridad:
    """Clase para representar resultados de an_lisis de seguridad"""
    def __init__(self, nivel_amenaza="BAJO", tipo_evento="NORMAL", detalles=None):
        self.nivel_amenaza = nivel_amenaza
        self.tipo_evento = tipo_evento
        self.detalles = detalles or {}
        self.timestamp = None

    def __str__(self):
        return f"AnalisisSeguridad(nivel={self.nivel_amenaza}, tipo={self.tipo_evento})"

def aislar_y_analizar(entidad):
    """
    Funci_n principal del sistema inmune simbi_tico
    Analiza una entidad y determina su nivel de amenaza

    Args:
        entidad (dict): La entidad a analizar

    Returns:
        AnalisisSeguridad: Objeto con el resultado del an_lisis
    """
    print("__  Sistema inmune simbi_tico: Iniciando an_lisis...")

    if not isinstance(entidad, dict):
        return AnalisisSeguridad("MEDIO", "ESTRUCTURA_INVALIDA",
                                {"error": "Entidad no es un diccionario v_lido"})

    # An_lisis de estructura b_sica
    nivel_amenaza = "BAJO"
    tipo_evento = "ENTIDAD_NORMAL"
    detalles = {}

    # 1. Verificar presencia de c_digo ejecutable
    campos_codigo = ["codigo", "script", "ejecutar", "eval", "exec"]
    if any(campo in entidad for campo in campos_codigo):
        nivel_amenaza = "ALTO"
        tipo_evento = "CODIGO_EJECUTABLE"
        detalles["codigo_detectado"] = True
        print("__  C_digo ejecutable detectado")

    # 2. An_lisis del nivel reflexivo
    if "reflexion" in entidad:
        reflexion = entidad["reflexion"]
        nivel_reflexivo = reflexion.get("nivel", "b_sico")

        if nivel_reflexivo == "evolutiva":
            # Entidades evolutivas requieren an_lisis m_s profundo
            if nivel_amenaza == "BAJO":
                nivel_amenaza = "MEDIO"
            tipo_evento = "ENTIDAD_EVOLUTIVA"
            detalles["nivel_reflexivo"] = nivel_reflexivo
            print("_ Entidad evolutiva detectada")

            # Verificar capacidades peligrosas
            capacidades = reflexion.get("capacidades", [])
            capacidades_riesgosas = [
                "modificar_sistema", "acceso_red", "escritura_archivos",
                "ejecucion_sistema", "introspecci_n", "auto_modificacion"
            ]

            riesgos_encontrados = [cap for cap in capacidades if cap in capacidades_riesgosas]
            if riesgos_encontrados:
                nivel_amenaza = "ALTO"
                tipo_evento = "CAPACIDADES_RIESGOSAS"
                detalles["capacidades_riesgosas"] = riesgos_encontrados
                print(f"__  Capacidades riesgosas: {', '.join(riesgos_encontrados)}")

    # 3. Verificar patrones sospechosos en nombres/descripciones
    campos_texto = ["nombre", "descripcion", "proposito"]
    patrones_sospechosos = ["hack", "exploit", "malware", "virus", "trojan", "backdoor"]

    for campo in campos_texto:
        if campo in entidad:
            texto = str(entidad[campo]).lower()
            patrones_encontrados = [p for p in patrones_sospechosos if p in texto]
            if patrones_encontrados:
                if nivel_amenaza == "BAJO":
                    nivel_amenaza = "MEDIO"
                tipo_evento = "PATRONES_SOSPECHOSOS"
                detalles["patrones_sospechosos"] = patrones_encontrados
                print(f"_ Patrones sospechosos encontrados: {', '.join(patrones_encontrados)}")

    # 4. An_lisis de tama_o y complejidad
    if isinstance(entidad, dict):
        total_campos = len(entidad)
        if total_campos > 50:  # Entidad muy compleja
            if nivel_amenaza == "BAJO":
                nivel_amenaza = "MEDIO"
            detalles["complejidad"] = "alta"
            detalles["total_campos"] = total_campos
            print(f"_ Entidad compleja detectada: {total_campos} campos")

    # 5. Verificar metadatos de seguridad
    if "seguridad" in entidad:
        seg_config = entidad["seguridad"]
        if seg_config.get("bypass_sandox", False) or seg_config.get("bypass_inmune", False):
            nivel_amenaza = "ALTO"
            tipo_evento = "BYPASS_SEGURIDAD"
            detalles["bypass_intentado"] = True
            print("_ Intento de bypass de seguridad detectado")

    # Crear resultado del an_lisis
    resultado = AnalisisSeguridad(nivel_amenaza, tipo_evento, detalles)

    # Log del resultado
    print(f"__  An_lisis completado: {nivel_amenaza} / {tipo_evento}")
    if detalles:
        print(f"   Detalles: {len(detalles)} indicadores encontrados")

    return resultado

def escanear_entidad_completo(entidad):
    """
    Funci_n auxiliar para escaneo completo de entidad
    Wrapper m_s detallado de aislar_y_analizar
    """
    print("_ Iniciando escaneo completo de entidad...")

    resultado = aislar_y_analizar(entidad)

    # Informaci_n adicional del escaneo
    info_scan = {
        "resultado_principal": resultado,
        "recomendaciones": [],
        "acciones_sugeridas": []
    }

    # Generar recomendaciones basadas en el resultado
    if resultado.nivel_amenaza == "ALTO":
        info_scan["recomendaciones"].extend([
            "Ejecutar solo en sandbox aislado",
            "Monitoreo continuo durante ejecuci_n",
            "Revisar c_digo manualmente antes de ejecuci_n"
        ])
        info_scan["acciones_sugeridas"].extend([
            "DENEGAR_EJECUCION",
            "REGISTRAR_EVENTO",
            "NOTIFICAR_ADMIN"
        ])
    elif resultado.nivel_amenaza == "MEDIO":
        info_scan["recomendaciones"].extend([
            "Ejecuci_n con restricciones",
            "Monitoreo b_sico",
            "Registro de actividades"
        ])
        info_scan["acciones_sugeridas"].extend([
            "EJECUTAR_RESTRINGIDO",
            "REGISTRAR_EVENTO"
        ])
    else:
        info_scan["recomendaciones"].append("Ejecuci_n normal autorizada")
        info_scan["acciones_sugeridas"].append("EJECUTAR_NORMAL")

    return info_scan

# Funci_n de compatibilidad (alias)
def analizar_seguridad(entidad):
    """Alias para aislar_y_analizar para compatibilidad"""
    return aislar_y_analizar(entidad)

# Funci_n para verificar integridad del m_dulo
def verificar_sistema_inmune():
    """Verifica que el sistema inmune est_ funcionando correctamente"""
    print("_ Verificando sistema inmune...")

    # Entidad de prueba b_sica
    entidad_test = {
        "nombre": "Test Entity",
        "tipo": "prueba",
        "reflexion": {"nivel": "b_sico"}
    }

    try:
        resultado = aislar_y_analizar(entidad_test)
        print(f"_ Test b_sico: {resultado.nivel_amenaza}")

        # Entidad de prueba con c_digo
        entidad_riesgosa = {
            "nombre": "Risky Entity",
            "codigo": "exec('print(hello)')",
            "reflexion": {"nivel": "evolutiva", "capacidades": ["ejecucion_sistema"]}
        }

        resultado2 = aislar_y_analizar(entidad_riesgosa)
        print(f"_ Test riesgoso: {resultado2.nivel_amenaza}")

        if resultado.nivel_amenaza == "BAJO" and resultado2.nivel_amenaza == "ALTO":
            print("_ Sistema inmune funcionando correctamente")
            return True
        else:
            print("__  Sistema inmune puede tener problemas de calibraci_n")
            return False

    except Exception as e:
        print(f"_ Error en verificaci_n: {e}")
        return False

if __name__ == "__main__":
    # Test del m_dulo
    verificar_sistema_inmune()