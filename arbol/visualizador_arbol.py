"""
visualizador_arbol.py
Visualizador del _rbol geneal_gico de entidades LER
"""
import json
from typing import Any, Dict, List
import os
import sys

# ------------------------------------------------------------------ #
# Cargar el _rbol desde el archivo JSON
# ------------------------------------------------------------------ #
def cargar_arbol(ruta: str) -> Dict[str, Any]:
    """Carga el _rbol geneal_gico desde un archivo JSON."""
    try:
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: No se encontr_ el archivo {ruta}")
        # Crear un _rbol de ejemplo si no existe el archivo
        return crear_arbol_ejemplo()
    except json.JSONDecodeError as e:
        print(f"Error al leer el JSON: {e}")
        return {}

def crear_arbol_ejemplo() -> Dict[str, Any]:
    """Crea un _rbol de ejemplo para demostraci_n."""
    return {
        "nombre": "Entidades LER Primordiales",
        "glifo": "_",
        "descripcion": "Ra_z del _rbol geneal_gico de entidades",
        "nodos": [
            {
                "nombre": "Entidades de Primer Orden",
                "glifo": "_",
                "descripcion": "Entidades fundamentales del sistema",
                "nodos": [
                    {
                        "nombre": "Alfa",
                        "glifo": "_",
                        "descripcion": "Primera entidad creadora",
                        "nodos": [
                            {
                                "nombre": "Alfa-Beta",
                                "glifo": "__",
                                "descripcion": "Descendiente h_brido de Alfa",
                                "nodos": []
                            }
                        ]
                    },
                    {
                        "nombre": "Beta",
                        "glifo": "_",
                        "descripcion": "Segunda entidad creadora",
                        "nodos": [
                            {
                                "nombre": "Beta-Gamma",
                                "glifo": "__",
                                "descripcion": "Fusi_n de Beta y Gamma",
                                "nodos": []
                            }
                        ]
                    }
                ]
            },
            {
                "nombre": "Entidades de Segundo Orden",
                "glifo": "_",
                "descripcion": "Entidades derivadas del primer orden",
                "nodos": [
                    {
                        "nombre": "Gamma",
                        "glifo": "_",
                        "descripcion": "Entidad de transformaci_n",
                        "nodos": []
                    },
                    {
                        "nombre": "Delta",
                        "glifo": "_",
                        "descripcion": "Entidad de equilibrio",
                        "nodos": []
                    }
                ]
            }
        ]
    }

# ------------------------------------------------------------------ #
# Visualizaci_n en consola
# ------------------------------------------------------------------ #
def visualizar_consola(arbol: Dict[str, Any], nivel: int = 0) -> None:
    """Muestra el _rbol geneal_gico en la consola con formato jer_rquico."""
    indent = "  " * nivel
    prefijo = "__" if nivel > 0 else "_"
    print(f"{indent}{prefijo} {arbol['nombre']} ({arbol['glifo']}) - {arbol['descripcion']}")
    
    for i, nodo in enumerate(arbol.get('nodos', [])):
        es_ultimo = i == len(arbol['nodos']) - 1
        visualizar_consola(nodo, nivel + 1)

def mostrar_estadisticas(arbol: Dict[str, Any]) -> None:
    """Muestra estad_sticas del _rbol geneal_gico."""
    def contar_nodos(nodo: Dict[str, Any]) -> int:
        count = 1
        for hijo in nodo.get('nodos', []):
            count += contar_nodos(hijo)
        return count
    
    def calcular_profundidad(nodo: Dict[str, Any], nivel: int = 0) -> int:
        if not nodo.get('nodos'):
            return nivel
        return max(calcular_profundidad(hijo, nivel + 1) for hijo in nodo['nodos'])
    
    total_nodos = contar_nodos(arbol)
    profundidad = calcular_profundidad(arbol)
    
    print("\n" + "="*50)
    print("ESTAD_STICAS DEL _RBOL GENEAL_GICO")
    print("="*50)
    print(f"Total de entidades: {total_nodos}")
    print(f"Profundidad m_xima: {profundidad}")
    print(f"Entidad ra_z: {arbol['nombre']}")
    print("="*50)

# ------------------------------------------------------------------ #
# Visualizaci_n web (Flask)
# ------------------------------------------------------------------ #
def visualizar_web(arbol: Dict[str, Any]) -> None:
    """Crea una visualizaci_n web del _rbol geneal_gico usando Flask."""
    try:
        from flask import Flask, render_template_string
        
        app = Flask(__name__)
        
        # Template HTML mejorado
        template = """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>_rbol Geneal_gico de Entidades LER</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: #333;
                    margin: 0;
                    padding: 20px;
                    min-height: 100vh;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    background: rgba(255, 255, 255, 0.95);
                    border-radius: 15px;
                    padding: 30px;
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
                }
                h1 {
                    text-align: center;
                    color: #4a5568;
                    margin-bottom: 30px;
                    font-size: 2.5em;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
                }
                .tree {
                    font-family: monospace;
                    font-size: 16px;
                    line-height: 1.6;
                }
                .node {
                    margin: 8px 0;
                    padding: 10px;
                    background: rgba(108, 117, 125, 0.1);
                    border-left: 4px solid #6c757d;
                    border-radius: 5px;
                    transition: all 0.3s ease;
                }
                .node:hover {
                    background: rgba(108, 117, 125, 0.2);
                    transform: translateX(5px);
                }
                .level-0 { border-left-color: #e74c3c; background: rgba(231, 76, 60, 0.1); }
                .level-1 { border-left-color: #3498db; background: rgba(52, 152, 219, 0.1); }
                .level-2 { border-left-color: #2ecc71; background: rgba(46, 204, 113, 0.1); }
                .level-3 { border-left-color: #f39c12; background: rgba(243, 156, 18, 0.1); }
                .glifo {
                    font-size: 1.2em;
                    margin-right: 8px;
                }
                .nombre {
                    font-weight: bold;
                    color: #2c3e50;
                }
                .descripcion {
                    color: #7f8c8d;
                    font-style: italic;
                    margin-left: 20px;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>_ _rbol Geneal_gico de Entidades LER</h1>
                <div class="tree">
                    {{ render_tree(arbol, 0) | safe }}
                </div>
            </div>
        </body>
        </html>
        """
        
        def render_tree(nodo, nivel):
            indent = "&nbsp;" * (nivel * 4)
            html = f'''
            <div class="node level-{nivel % 4}">
                {indent}<span class="glifo">{nodo['glifo']}</span>
                <span class="nombre">{nodo['nombre']}</span>
                <div class="descripcion">{indent}&nbsp;&nbsp;{nodo['descripcion']}</div>
            </div>
            '''
            for hijo in nodo.get('nodos', []):
                html += render_tree(hijo, nivel + 1)
            return html
        
        @app.route('/')
        def index():
            return render_template_string(template, arbol=arbol, render_tree=render_tree)
        
        print("_ Iniciando servidor web en http://localhost:8080")
        print("_ Presiona Ctrl+C para detener el servidor")
        app.run(host='0.0.0.0', port=8080, debug=False)
        
    except ImportError:
        print("_ Flask no est_ instalado.")
        print("_ Inst_lalo con: pip install flask")
        print("_ Mostrando visualizaci_n en consola...")
        visualizar_consola(arbol)

# ------------------------------------------------------------------ #
# Exportar a otros formatos
# ------------------------------------------------------------------ #
def exportar_a_texto(arbol: Dict[str, Any], ruta_salida: str) -> None:
    """Exporta el _rbol a un archivo de texto plano."""
    def arbol_a_texto(nodo: Dict[str, Any], nivel: int = 0) -> str:
        indent = "  " * nivel
        texto = f"{indent}_ {nodo['nombre']} ({nodo['glifo']}) - {nodo['descripcion']}\n"
        for hijo in nodo.get('nodos', []):
            texto += arbol_a_texto(hijo, nivel + 1)
        return texto
    
    with open(ruta_salida, 'w', encoding='utf-8') as f:
        f.write("_RBOL GENEAL_GICO DE ENTIDADES LER\n")
        f.write("="*50 + "\n\n")
        f.write(arbol_a_texto(arbol))
    
    print(f"_ _rbol exportado a: {ruta_salida}")

# ------------------------------------------------------------------ #
# Gesti_n de m_ltiples archivos
# ------------------------------------------------------------------ #
def listar_archivos_json(directorio: str) -> List[str]:
    """Lista todos los archivos JSON en el directorio especificado."""
    archivos = []
    if os.path.exists(directorio):
        for archivo in os.listdir(directorio):
            if archivo.endswith('.json'):
                archivos.append(archivo)
    return sorted(archivos)

def seleccionar_archivo(archivos: List[str]) -> str:
    """Permite al usuario seleccionar un archivo de la lista."""
    if len(archivos) == 0:
        print("_ No se encontraron archivos JSON en el directorio 'arbol/'")
        return None
    
    if len(archivos) == 1:
        print(f"_ Usando el _nico archivo encontrado: {archivos[0]}")
        return archivos[0]
    
    print("\n_ Archivos JSON disponibles:")
    print("-" * 30)
    for i, archivo in enumerate(archivos, 1):
        print(f"  {i}. {archivo}")
    print("-" * 30)
    
    while True:
        try:
            seleccion = input(f"Selecciona un archivo (1-{len(archivos)}) o presiona Enter para usar {archivos[0]}: ").strip()
            
            if seleccion == "":
                return archivos[0]  # Usar el primero por defecto
            
            indice = int(seleccion) - 1
            if 0 <= indice < len(archivos):
                return archivos[indice]
            else:
                print(f"_ Por favor, ingresa un n_mero entre 1 y {len(archivos)}")
        
        except ValueError:
            print("_ Por favor, ingresa un n_mero v_lido")
        except KeyboardInterrupt:
            print("\n_ Operaci_n cancelada")
            return None

def mostrar_info_archivos(directorio: str) -> None:
    """Muestra informaci_n sobre todos los archivos JSON disponibles."""
    archivos = listar_archivos_json(directorio)
    
    if not archivos:
        print("_ No se encontraron archivos JSON en el directorio 'arbol/'")
        return
    
    print(f"\n_ INFORMACI_N DE ARCHIVOS JSON ({len(archivos)} encontrados)")
    print("=" * 60)
    
    for archivo in archivos:
        ruta_completa = os.path.join(directorio, archivo)
        try:
            arbol = cargar_arbol(ruta_completa)
            if arbol:
                def contar_nodos(nodo):
                    count = 1
                    for hijo in nodo.get('nodos', []):
                        count += contar_nodos(hijo)
                    return count
                
                total_nodos = contar_nodos(arbol)
                tama_o_kb = os.path.getsize(ruta_completa) / 1024
                
                print(f"_ {archivo}")
                print(f"   __ Nombre: {arbol.get('nombre', 'Sin nombre')}")
                print(f"   __ Entidades: {total_nodos}")
                print(f"   __ Tama_o: {tama_o_kb:.1f} KB")
                print(f"   __ Descripci_n: {arbol.get('descripcion', 'Sin descripci_n')}")
                print()
        except Exception as e:
            print(f"_ {archivo} - Error al leer: {e}")
            print()

# ------------------------------------------------------------------ #
# CLI mejorada
# ------------------------------------------------------------------ #
def mostrar_ayuda():
    """Muestra la ayuda del programa."""
    print("""
_ VISUALIZADOR DE _RBOL GENEAL_GICO LER
=====================================

Uso:
    python visualizador_arbol.py [comando] [archivo] [opciones]

Comandos disponibles:
    (sin comando)  - Visualizaci_n en consola (modo interactivo)
    web [archivo]  - Visualizaci_n en navegador web
    stats [archivo] - Mostrar estad_sticas del _rbol
    export [archivo] [salida] - Exportar a archivo de texto
    list          - Listar todos los archivos JSON disponibles
    info          - Mostrar informaci_n detallada de todos los archivos
    help          - Mostrar esta ayuda

Ejemplos:
    python visualizador_arbol.py
    python visualizador_arbol.py web arbol_ler.json
    python visualizador_arbol.py stats genealogia.json
    python visualizador_arbol.py export estructura_arbol.json output.txt
    python visualizador_arbol.py list
    python visualizador_arbol.py info
    
Archivos esperados en ./arbol/:
    - arbol_ler.json
    - estructura_arbol.json  
    - genealogia.json
    """)

if __name__ == "__main__":
    directorio_arbol = "arbol"
    
    # Crear directorio si no existe
    os.makedirs(directorio_arbol, exist_ok=True)
    
    # Procesar argumentos de l_nea de comandos
    if len(sys.argv) == 1:
        # Modo interactivo: mostrar archivos disponibles y permitir selecci_n
        print("_ VISUALIZADOR DE _RBOL GENEAL_GICO LER")
        print("="*50)
        
        archivos = listar_archivos_json(directorio_arbol)
        archivo_seleccionado = seleccionar_archivo(archivos)
        
        if not archivo_seleccionado:
            print("_ No se pudo seleccionar un archivo.")
            sys.exit(1)
        
        ruta_arbol = os.path.join(directorio_arbol, archivo_seleccionado)
        arbol = cargar_arbol(ruta_arbol)
        
        if arbol:
            print(f"\n_ Visualizando: {archivo_seleccionado}")
            print("="*50)
            visualizar_consola(arbol)
            mostrar_estadisticas(arbol)
        else:
            print("_ Error: No se pudo cargar el _rbol geneal_gico.")
            sys.exit(1)
    
    elif sys.argv[1] == "list":
        # Listar archivos disponibles
        archivos = listar_archivos_json(directorio_arbol)
        print(f"\n_ Archivos JSON en '{directorio_arbol}/' ({len(archivos)} encontrados):")
        print("-" * 40)
        for i, archivo in enumerate(archivos, 1):
            print(f"  {i}. {archivo}")
        if not archivos:
            print("  (ning_n archivo encontrado)")
        print()
    
    elif sys.argv[1] == "info":
        # Mostrar informaci_n detallada de todos los archivos
        mostrar_info_archivos(directorio_arbol)
    
    elif sys.argv[1] == "help":
        mostrar_ayuda()
    
    else:
        # Otros comandos que requieren un archivo
        comando = sys.argv[1]
        
        # Determinar archivo a usar
        if len(sys.argv) > 2 and not sys.argv[2].startswith('-'):
            archivo_especificado = sys.argv[2]
            ruta_arbol = os.path.join(directorio_arbol, archivo_especificado)
        else:
            # Si no se especifica archivo, usar modo interactivo
            archivos = listar_archivos_json(directorio_arbol)
            archivo_seleccionado = seleccionar_archivo(archivos)
            
            if not archivo_seleccionado:
                print("_ No se pudo seleccionar un archivo.")
                sys.exit(1)
            
            ruta_arbol = os.path.join(directorio_arbol, archivo_seleccionado)
        
        # Cargar el _rbol
        arbol = cargar_arbol(ruta_arbol)
        
        if not arbol:
            print("_ Error: No se pudo cargar el _rbol geneal_gico.")
            sys.exit(1)
        
        # Ejecutar comando
        if comando == "web":
            print(f"_ Iniciando visualizaci_n web de: {os.path.basename(ruta_arbol)}")
            visualizar_web(arbol)
            
        elif comando == "stats":
            print(f"_ Estad_sticas de: {os.path.basename(ruta_arbol)}")
            mostrar_estadisticas(arbol)
            
        elif comando == "export":
            # Determinar archivo de salida
            if len(sys.argv) > 3:
                ruta_salida = sys.argv[3]
            elif len(sys.argv) > 2 and sys.argv[2].endswith('.txt'):
                ruta_salida = sys.argv[2]
            else:
                nombre_base = os.path.splitext(os.path.basename(ruta_arbol))[0]
                ruta_salida = f"{nombre_base}_export.txt"
            
            print(f"_ Exportando {os.path.basename(ruta_arbol)} a {ruta_salida}")
            exportar_a_texto(arbol, ruta_salida)
            
        else:
            print(f"_ Comando desconocido: {comando}")
            mostrar_ayuda()