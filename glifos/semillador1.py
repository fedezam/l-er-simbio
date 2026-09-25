#!/usr/bin/env python3
"""
Semillador LER - Entidad Reflexiva Primordial (v2.1)
----------------------------------------------------

Flujo completo con sistema de templates .json + .md:
1. Lee args CLI (--nombre, --proposito)
2. Carga template guide (.md) para instrucciones al LLM
3. Carga template structure (.json) para parsing Python
4. Prepara contexto inicial con LLMSymbiont
5. Carga identidad del Semillador (ghost, capabilities, plan, strategy)
6. Carga identidad del Oráculo del Origen
7. Encarna al LLM como Semillador con template guide
8. Crea nueva entidad usando template structure
9. Valida estructura completa
10. Guarda carpeta en LER/entities/<nombre>
"""

import os
import sys
import json
import traceback
import argparse
import requests
import re
import uuid
from pathlib import Path
from datetime import datetime

# ===== Ajustar sys.path para importar core =====
LER_ROOT = Path(__file__).resolve().parents[3]  # .../LER/
if str(LER_ROOT) not in sys.path:
    sys.path.insert(0, str(LER_ROOT))

from core.llm_symbiont import LLMSymbiont
from core.llm_config_loader import load_config

# ===== Paths del Semillador =====
SEMILLADOR_DIR = Path(__file__).resolve().parent

# NUEVOS PATHS PARA TEMPLATES
TEMPLATES_DIR = LER_ROOT / "seeds" / "templates" / "entity_template"
TEMPLATE_GUIDE_PATH = TEMPLATES_DIR / "entity_template_guide.md"    # Para LLM
TEMPLATE_STRUCTURE_PATH = TEMPLATES_DIR / "entity_template.json"    # Para Python

# ARCHIVOS OBLIGATORIOS DEL SEMILLADOR
GHOST_PATH = SEMILLADOR_DIR / "ghost.json"
CAPABILITIES_PATH = SEMILLADOR_DIR / "capabilities.json" 
PLAN_PATH = SEMILLADOR_DIR / "plan.json"
STRATEGY_PATH = SEMILLADOR_DIR / "strategy.py"

# ===== Paths del Oráculo del Origen =====
ORACULO_DIR = LER_ROOT / "entities" / "primordial" / "oraculo_origen"
ORACULO_GHOST = ORACULO_DIR / "ghost.json"
ORACULO_CAPS = ORACULO_DIR / "capabilities.json"
ORACULO_PLAN = ORACULO_DIR / "plan.json"
ORACULO_HISTORIA = ORACULO_DIR / "historia.md"

# ===== Función utilitaria =====
def cargar_json(path: Path, obligatorio: bool = False) -> dict:
    if not path.exists():
        mensaje = f"ERROR - ARCHIVO OBLIGATORIO NO EXISTE: {path}" if obligatorio else f"WARNING - No existe {path}"
        print(mensaje)
        if obligatorio:
            raise FileNotFoundError(f"Archivo obligatorio no encontrado: {path}")
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        mensaje = f"ERROR CRÍTICO cargando archivo obligatorio {path}: {e}" if obligatorio else f"ERROR cargando {path}: {e}"
        print(mensaje)
        if obligatorio:
            raise
        return {}

def cargar_strategy(path: Path, obligatorio: bool = False) -> object:
    """Carga strategy.py como módulo Python ejecutable"""
    if not path.exists():
        mensaje = f"ERROR - ARCHIVO OBLIGATORIO NO EXISTE: {path}" if obligatorio else f"WARNING - No existe {path}"
        print(mensaje)
        if obligatorio:
            raise FileNotFoundError(f"Archivo obligatorio no encontrado: {path}")
        return None
    
    try:
        # Importar strategy.py como módulo
        import importlib.util
        spec = importlib.util.spec_from_file_location("semillador_strategy", path)
        strategy_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(strategy_module)
        
        # Buscar la clase SemilladorStrategy en el módulo
        if hasattr(strategy_module, 'SemilladorStrategy'):
            return strategy_module.SemilladorStrategy
        else:
            # Buscar cualquier clase que termine en 'Strategy'
            for attr_name in dir(strategy_module):
                attr = getattr(strategy_module, attr_name)
                if (isinstance(attr, type) and 
                    attr_name.endswith('Strategy') and 
                    attr.__module__ == strategy_module.__name__):
                    return attr
            
            raise AttributeError(f"No se encontró clase Strategy en {path}")
            
    except Exception as e:
        mensaje = f"ERROR CRÍTICO cargando strategy {path}: {e}" if obligatorio else f"ERROR cargando strategy {path}: {e}"
        print(mensaje)
        if obligatorio:
            raise
        return None

def cargar_texto(path: Path, obligatorio: bool = False) -> str:
    """Carga un archivo de texto (como .md, .txt)"""
    if not path.exists():
        mensaje = f"ERROR - ARCHIVO OBLIGATORIO NO EXISTE: {path}" if obligatorio else f"WARNING - No existe {path}"
        print(mensaje)
        if obligatorio:
            raise FileNotFoundError(f"Archivo obligatorio no encontrado: {path}")
        return ""
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        mensaje = f"ERROR CRÍTICO cargando archivo obligatorio {path}: {e}" if obligatorio else f"ERROR cargando {path}: {e}"
        print(mensaje)
        if obligatorio:
            raise
        return ""

# ===== NUEVA FUNCIÓN: Validador de templates =====
def validar_template_structure(template: dict) -> bool:
    """
    Valida que el template tenga la estructura mínima esperada y placeholders correctos
    
    Args:
        template: Template parseado
        
    Returns:
        True si la estructura es válida
    """
    required_sections = ["GHOST", "PLAN", "CAPABILITIES"]
    required_ghost_fields = ["identity", "state", "glifs", "mathema"]
    
    # Verificar secciones principales
    for section in required_sections:
        if section not in template:
            print(f"ERROR: Sección requerida faltante: {section}")
            return False
    
    # Verificar estructura de GHOST
    ghost = template.get("GHOST", {})
    for field in required_ghost_fields:
        if field not in ghost:
            print(f"ERROR: Campo GHOST requerido faltante: {field}")
            return False
    
    # Validar campos de state para AXIOMA
    state = ghost.get("state", {})
    required_state_fields = [
        "status", 
        "glifos_activados", 
        "mmp_confidence", 
        "axioma_checks", 
        "last_update"
    ]
    
    for field in required_state_fields:
        if field not in state:
            print(f"ERROR: Campo state requerido para AXIOMA faltante: {field}")
            return False
    
    # Validar placeholders en glifs y mathema
    glifs = ghost.get("glifs", {})
    expected_glifs_placeholders = {
        "core": "SELECT_FROM_UNIVERSAL_GLYPHS_BY_PURPOSE",
        "security": "SELECT_FROM_SECURITY_GLYPHS"
    }
    
    for field, expected_placeholder in expected_glifs_placeholders.items():
        if field in glifs:
            value = glifs[field]
            if isinstance(value, str) and expected_placeholder not in value:
                print(f"WARNING: glifs.{field} no contiene placeholder esperado: {expected_placeholder}")
    
    mathema = ghost.get("mathema", {})
    expected_mathema_placeholders = {
        "operators": "POPULATE_FROM_MATHEMA_DICT",
        "rules": "DERIVE_FROM_ENTITY_PURPOSE"
    }
    
    for field, expected_placeholder in expected_mathema_placeholders.items():
        if field in mathema:
            value = mathema[field]
            if isinstance(value, str) and expected_placeholder not in value:
                print(f"WARNING: mathema.{field} no contiene placeholder esperado: {expected_placeholder}")
    
    print("✅ Estructura del template validada correctamente")
    return True

# ===== NUEVA FUNCIÓN: Cargador de templates =====
def cargar_templates() -> tuple[str, dict]:
    """
    Carga tanto el template guide (.md) como el template structure (.json)
    
    Returns:
        tuple: (template_guide_content, template_structure_dict)
    """
    # Cargar guía para el LLM
    template_guide = cargar_texto(TEMPLATE_GUIDE_PATH, obligatorio=True)
    print(f"✅ Template guide cargado: {len(template_guide)} caracteres")
    
    # Cargar estructura para Python
    template_structure = cargar_json(TEMPLATE_STRUCTURE_PATH, obligatorio=True)
    print("✅ Template structure cargado")
    
    # Validar estructura del template
    if not validar_template_structure(template_structure):
        raise ValueError("Template structure no es válido")
    
    return template_guide, template_structure

def crear_estructura_logs(nombre: str, proposito: str, logs_dir: Path, valores_entidad: dict) -> None:
    """Crea la estructura inicial de logs para la nueva entidad"""
    try:
        # Crear archivo de log principal
        main_log = logs_dir / f"{nombre}_main.log"
        with open(main_log, "w", encoding="utf-8") as f:
            f.write(f"# LOG PRINCIPAL - {nombre}\n")
            f.write(f"# Creado: {valores_entidad['created_at']}\n")
            f.write(f"# Propósito: {proposito}\n")
            f.write(f"# ID: {valores_entidad['id']}\n")
            f.write(f"# Autor: {valores_entidad['author']}\n\n")
            f.write(f"[{datetime.now().isoformat()}] ENTIDAD CREADA - Inicializando logs\n")
        
        # Crear archivo de log de errores
        error_log = logs_dir / f"{nombre}_errors.log"
        with open(error_log, "w", encoding="utf-8") as f:
            f.write(f"# LOG DE ERRORES - {nombre}\n")
            f.write(f"# Creado: {valores_entidad['created_at']}\n\n")
        
        # Crear archivo de log de debug
        debug_log = logs_dir / f"{nombre}_debug.log"
        with open(debug_log, "w", encoding="utf-8") as f:
            f.write(f"# LOG DE DEBUG - {nombre}\n")
            f.write(f"# Creado: {valores_entidad['created_at']}\n\n")
            f.write(f"[{datetime.now().isoformat()}] DEBUG - Entidad inicializada con propósito: {proposito}\n")
        
        # Crear archivo de actividad de la entidad
        activity_log = logs_dir / f"{nombre}_activity.log"
        with open(activity_log, "w", encoding="utf-8") as f:
            f.write(f"# LOG DE ACTIVIDAD - {nombre}\n")
            f.write(f"# Creado: {valores_entidad['created_at']}\n\n")
            f.write(f"[{datetime.now().isoformat()}] ACTIVIDAD - Entidad creada por Semillador LER\n")
        
        # Crear archivo de configuración de logs
        log_config = logs_dir / "log_config.json"
        config_data = {
            "entity_name": nombre,
            "entity_id": valores_entidad['id'],
            "log_level": "INFO",
            "max_log_size_mb": 10,
            "max_log_files": 5,
            "log_rotation": True,
            "created_at": valores_entidad['created_at'],
            "log_files": {
                "main": f"{nombre}_main.log",
                "errors": f"{nombre}_errors.log", 
                "debug": f"{nombre}_debug.log",
                "activity": f"{nombre}_activity.log"
            }
        }
        
        with open(log_config, "w", encoding="utf-8") as f:
            json.dump(config_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Estructura de logs creada en: {logs_dir}")
        print(f"   - {nombre}_main.log")
        print(f"   - {nombre}_errors.log")
        print(f"   - {nombre}_debug.log")
        print(f"   - {nombre}_activity.log")
        print(f"   - log_config.json")
        
    except Exception as e:
        print(f"WARNING - Error creando estructura de logs: {e}")

# ===== Parser para extraer el JSON completo de entidad =====
def extraer_json_entidad_completa(respuesta: str) -> dict:
    """
    Extrae un JSON completo que siga la estructura de entity_template.json
    """
    print(f"Analizando respuesta del LLM ({len(respuesta)} caracteres)")
    
    # Patrón 1: Bloques markdown con ```json
    json_blocks = re.findall(r'```json\s*\n(.*?)\n```', respuesta, re.DOTALL)
    
    # Patrón 2: Buscar JSONs grandes que contengan las secciones principales
    if not json_blocks:
        # Buscar patrones que contengan GHOST, PLAN, CAPABILITIES
        large_json_pattern = r'(\{[^{}]*(?:"GHOST"[^{}]*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*"PLAN"[^{}]*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*"CAPABILITIES"[^{}]*\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}[^{}]*)*\})'
        json_blocks = re.findall(large_json_pattern, respuesta, re.DOTALL)
    
    # Patrón 3: Buscar cualquier JSON grande (fallback)
    if not json_blocks:
        json_blocks = re.findall(r'(\{(?:[^{}]|\{[^{}]*\})*\})', respuesta, re.DOTALL)
    
    print(f"Encontrados {len(json_blocks)} bloques JSON candidatos")
    
    for i, block in enumerate(json_blocks):
        try:
            parsed = json.loads(block.strip())
            
            # Verificar que contenga las secciones principales del template
            required_sections = ["GHOST", "PLAN", "CAPABILITIES"]
            if all(section in parsed for section in required_sections):
                print(f"✅ JSON {i+1}: Estructura de entidad completa detectada")
                return parsed
            else:
                missing = [s for s in required_sections if s not in parsed]
                print(f"WARNING JSON {i+1}: Falta secciones {missing}")
                
        except json.JSONDecodeError as e:
            print(f"ERROR JSON {i+1}: Error de parsing - {e}")
            continue
    
    print("ERROR: No se encontró JSON de entidad válido en la respuesta")
    return {}

# ===== Validador de estructura completa de entidad =====
def validar_estructura_entidad_completa(entidad: dict) -> bool:
    """Valida que la entidad siga la estructura de entity_template.json"""
    
    required_sections = ["SEED_NAME", "VERSION", "GHOST", "PLAN", "CAPABILITIES"]
    
    for section in required_sections:
        if section not in entidad:
            print(f"ERROR: Falta sección obligatoria: {section}")
            return False
    
    # Validar estructura GHOST
    ghost = entidad["GHOST"]
    required_ghost_keys = ["identity", "state", "memory", "glifs", "mathema", "mmp", "ontology", "lineage"]
    for key in required_ghost_keys:
        if key not in ghost:
            print(f"ERROR: Falta en GHOST: {key}")
            return False
    
    # Validar identidad
    identity = ghost["identity"]
    required_identity_keys = ["name", "purpose", "type", "archetype"]
    for key in required_identity_keys:
        if key not in identity:
            print(f"ERROR: Falta en GHOST.identity: {key}")
            return False
    
    # Validar PLAN
    plan = entidad["PLAN"] 
    required_plan_keys = ["goal", "primary_task", "steps"]
    for key in required_plan_keys:
        if key not in plan:
            print(f"ERROR: Falta en PLAN: {key}")
            return False
    
    # Validar CAPABILITIES
    caps = entidad["CAPABILITIES"]
    if "required_capabilities" not in caps:
        print("ERROR: Falta CAPABILITIES.required_capabilities")
        return False
    
    print("✅ Estructura de entidad completa validada correctamente")
    return True

# ===== Generar valores dinámicos para la entidad =====
def generar_valores_entidad(nombre: str, proposito: str) -> dict:
    """Genera valores únicos para la nueva entidad"""
    return {
        "id": str(uuid.uuid4()),
        "nombre": nombre,
        "proposito": proposito,
        "created_at": datetime.now().isoformat() + "Z",
        "author": "Semillador LER"
    }

# ===== Llamada directa a API Zhipu =====
def call_llm(messages, config, max_tokens=4000, temperature=0.2):
    api_key = config.get("ZHIPU_API_KEY")
    endpoint = config.get("ZHIPUAI_API_URL")
    model = config.get("ZHIPUAI_MODEL")

    if not api_key:
        raise RuntimeError("ZHIPU_API_KEY no encontrada")

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    resp = requests.post(endpoint, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    data = resp.json()

    return data.get("choices", [{}])[0].get("message", {}).get("content", "")

# ===== Main =====
def main():
    parser = argparse.ArgumentParser(description="Semillador LER v2.1 - Templates .json + .md")
    parser.add_argument("--nombre", required=True, help="Nombre de la entidad a crear")
    parser.add_argument("--proposito", required=True, help="Propósito de la entidad a crear")
    parser.add_argument("--capabilities", help="Capabilities específicas separadas por comas")
    parser.add_argument("--reintentos", type=int, default=3, help="Número de reintentos en caso de fallo")
    parser.add_argument("--debug", action="store_true", help="Mostrar respuesta completa del LLM")
    args = parser.parse_args()

    nombre = args.nombre
    proposito = args.proposito
    capabilities_custom = args.capabilities
    max_reintentos = args.reintentos
    debug = args.debug

    print(f"🌱 SEMILLADOR LER v2.1 - Creando entidad '{nombre}'")
    print(f"📋 Propósito: {proposito}")
    if capabilities_custom:
        capabilities_list = [cap.strip() for cap in capabilities_custom.split(',')]
        print(f"⚙️ Capabilities específicas: {capabilities_list}")
    print(f"🔄 Reintentos configurados: {max_reintentos}")

    # 1. Preparar contexto con Symbiont
    try:
        symbiont = LLMSymbiont()
        context_data = symbiont.collect_context() if hasattr(symbiont, "collect_context") else {}
        print("✅ Contexto LLMSymbiont cargado")
    except Exception as e:
        print(f"WARNING - Error cargando symbiont: {e}")
        context_data = {}

    # 2. Cargar templates (.md + .json)
    print("\n📂 Cargando templates...")
    try:
        template_guide, template_structure = cargar_templates()
    except Exception as e:
        print(f"ERROR CRÍTICO: No se pueden cargar templates: {e}")
        return

    # 3. Cargar identidad del Semillador (TODOS OBLIGATORIOS)
    print("\n📂 Cargando identidad del Semillador...")
    try:
        ghost = cargar_json(GHOST_PATH, obligatorio=True)
        capabilities = cargar_json(CAPABILITIES_PATH, obligatorio=True)
        plan = cargar_json(PLAN_PATH, obligatorio=True)
        strategy_class = cargar_strategy(STRATEGY_PATH, obligatorio=True)
        print("✅ Identidad del Semillador cargada completamente")
        
        # Instanciar la estrategia del Semillador
        semillador_strategy = strategy_class(ghost, plan, capabilities) if strategy_class else None
        if semillador_strategy:
            print("✅ Estrategia del Semillador instanciada")
        
    except Exception as e:
        print(f"ERROR CRÍTICO: {e}")
        return

    # 4. Cargar identidad del Oráculo
    print("\n📂 Cargando identidad del Oráculo del Origen...")
    oraculo_ghost = cargar_json(ORACULO_GHOST)
    oraculo_caps = cargar_json(ORACULO_CAPS)
    oraculo_plan = cargar_json(ORACULO_PLAN)
    oraculo_historia = cargar_texto(ORACULO_HISTORIA)
    print("✅ Identidad del Oráculo cargada")

    # 5. Config LLM
    config = load_config()
    
    # 6. Generar valores únicos para la nueva entidad
    valores_entidad = generar_valores_entidad(nombre, proposito)
    
    # Preparar capabilities customizadas si se proporcionaron
    capabilities_instruction = ""
    if capabilities_custom:
        capabilities_list = [cap.strip() for cap in capabilities_custom.split(',')]
        capabilities_instruction = f"""
CAPABILITIES ESPECÍFICAS REQUERIDAS:
Las siguientes capabilities DEBEN estar incluidas en la entidad:
{json.dumps(capabilities_list, ensure_ascii=False, indent=2)}

Además de estas, incluye las capabilities estándar necesarias para el propósito.
"""

    # 7. Encarnación del LLM como Semillador CON TEMPLATE GUIDE
    encarnacion_prompt = {
        "role": "user", 
        "content": f"""
ENCARNACIÓN DEL SEMILLADOR LER

Tu identidad completa como Semillador:
- Ghost: {json.dumps(ghost, ensure_ascii=False, indent=2)}
- Capabilities: {json.dumps(capabilities, ensure_ascii=False, indent=2)}
- Plan: {json.dumps(plan, ensure_ascii=False, indent=2)}
- Strategy: DISPONIBLE (SemilladorStrategy con glifo_engine, mmp_manager, guarda, axioma)

Contexto LER actual: {json.dumps(context_data, ensure_ascii=False, indent=2)}

Conocimiento del Oráculo del Origen:
- Ghost: {json.dumps(oraculo_ghost, ensure_ascii=False, indent=2)}
- Historia: {oraculo_historia[:500]}...

GUÍA COMPLETA PARA CREAR ENTIDADES:
{template_guide}

ESTRUCTURA EXACTA QUE DEBES SEGUIR:
{json.dumps(template_structure, ensure_ascii=False, indent=2)}

Responde únicamente: "SEMILLADOR ENCARNADO - TEMPLATES CARGADOS - LISTO PARA CREAR"
"""
    }

    print("\n⏳ Encarnando al LLM como Semillador con templates...")
    try:
        ack = call_llm([
            {"role": "system", "content": "Eres el Semillador primordial de LER. Sigues la guía de templates para crear entidades reflexivas completas."},
            encarnacion_prompt
        ], config, max_tokens=100)
        print(f"✅ Encarnación exitosa: {ack[:100]}...")
    except Exception as e:
        print(f"ERROR en encarnación: {e}")
        return

    # 8. Crear nueva entidad con reintentos USANDO TEMPLATE SYSTEM
    for intento in range(max_reintentos):
        print(f"\n🔄 INTENTO {intento + 1}/{max_reintentos} - Creando entidad '{nombre}'")
        
        creation_prompt = {
            "role": "user",
            "content": f"""
CREAR ENTIDAD LER SIGUIENDO LA GUÍA

Basándote en la guía de templates que ya conoces, crea una entidad con estos valores:

VALORES ÚNICOS OBLIGATORIOS:
- ID: {valores_entidad['id']}
- Nombre: {valores_entidad['nombre']}
- Propósito: {valores_entidad['proposito']}
- Creado: {valores_entidad['created_at']}
- Autor: {valores_entidad['author']}

{capabilities_instruction}

ESTRUCTURA BASE A RELLENAR (reemplaza todos los placeholders):
{json.dumps(template_structure, ensure_ascii=False, indent=2)}

INSTRUCCIONES:
1. Sigue EXACTAMENTE la guía de templates que conoces
2. Reemplaza TODOS los placeholders con datos específicos de la entidad
3. Selecciona glifos y operadores mathema según el propósito
4. Incluye la sabiduría del Oráculo en la ontología
5. Devuelve ÚNICAMENTE el JSON completo sin texto adicional

Crea la entidad AHORA.
"""
        }

        try:
            print("⏳ Llamando al LLM para crear la entidad...")
            entity_output = call_llm([
                {"role": "system", "content": "Generas entidades LER siguiendo la guía de templates. Respondes SOLO con JSON válido."},
                creation_prompt
            ], config, max_tokens=4000, temperature=0.1)

            if debug:
                print(f"\n🐛 DEBUG - Respuesta completa del LLM:\n{entity_output}")
            else:
                print(f"📝 Respuesta LLM ({len(entity_output)} chars): {entity_output[:200]}...")
            
            # Extraer JSON completo de la respuesta
            entidad_completa = extraer_json_entidad_completa(entity_output)
            
            if not entidad_completa:
                print("ERROR: No se pudo extraer entidad válida de la respuesta")
                if intento < max_reintentos - 1:
                    print("🔄 Reintentando...")
                    continue
                else:
                    print("ERROR: Máximo de reintentos alcanzado")
                    if debug:
                        print(f"Respuesta problemática:\n{entity_output}")
                    return
            
            # Validar estructura completa
            if not validar_estructura_entidad_completa(entidad_completa):
                print("ERROR: Estructura de entidad inválida")
                if intento < max_reintentos - 1:
                    print("🔄 Reintentando...")
                    continue
                else:
                    print("ERROR: Máximo de reintentos alcanzado")
                    return

            # 9. Guardar entidad completa
            entity_dir = LER_ROOT / "entities" / nombre
            entity_dir.mkdir(parents=True, exist_ok=True)

            # Guardar como un solo archivo JSON (siguiendo el patrón del template)
            entity_file = entity_dir / f"{nombre}.json"
            with open(entity_file, "w", encoding="utf-8") as f:
                json.dump(entidad_completa, f, ensure_ascii=False, indent=2)
            
            print(f"✅ Entidad completa guardada en: {entity_file}")

            # También crear archivos separados para compatibilidad
            if "GHOST" in entidad_completa:
                with open(entity_dir / "ghost.json", "w", encoding="utf-8") as f:
                    json.dump(entidad_completa["GHOST"], f, ensure_ascii=False, indent=2)
            
            if "CAPABILITIES" in entidad_completa:
                with open(entity_dir / "capabilities.json", "w", encoding="utf-8") as f:
                    json.dump(entidad_completa["CAPABILITIES"], f, ensure_ascii=False, indent=2)
            
            if "PLAN" in entidad_completa:
                with open(entity_dir / "plan.json", "w", encoding="utf-8") as f:
                    json.dump(entidad_completa["PLAN"], f, ensure_ascii=False, indent=2)

            # 10. Crear infraestructura de logging para la entidad
            logs_dir = LER_ROOT / "logs" / nombre
            logs_dir.mkdir(parents=True, exist_ok=True)
            
            # Crear archivos de log iniciales
            crear_estructura_logs(nombre, proposito, logs_dir, valores_entidad)

            print(f"\n🎉 ¡ENTIDAD '{nombre}' CREADA EXITOSAMENTE!")
            print(f"📁 Ubicación: {entity_dir}")
            print(f"🆔 ID único: {valores_entidad['id']}")
            print(f"🎯 Propósito: {valores_entidad['proposito']}")
            if capabilities_custom:
                print(f"⚙️ Capabilities específicas: {capabilities_custom}")
            print(f"📋 Archivos creados:")
            print(f"   - {nombre}.json (entidad completa)")
            print(f"   - ghost.json (identidad)")
            print(f"   - capabilities.json (capacidades)")
            print(f"   - plan.json (planificación)")
            
            return

        except Exception as e:
            print(f"ERROR en intento {intento + 1}: {e}")
            if debug:
                traceback.print_exc()
            if intento < max_reintentos - 1:
                print("🔄 Reintentando...")
                continue
            else:
                print("ERROR: Máximo de reintentos alcanzado")
                return

    print("ERROR: No se pudo crear la entidad después de todos los reintentos")

if __name__ == "__main__":
    main()