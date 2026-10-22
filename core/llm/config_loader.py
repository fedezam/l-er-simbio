import os
from pathlib import Path

def load_env():
    """Carga las variables del archivo .env en el entorno del sistema."""
    env_path = Path(__file__).parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    os.environ[key.strip()] = val.strip()
        print("✅ Archivo .env cargado correctamente.")
    else:
        print("⚠️  No se encontró el archivo .env. Usando variables del sistema.")

def get_api_key(provider="openrouter"):
    """Devuelve la clave de API según el proveedor."""
    load_env()
    keys = {
        "openrouter": os.environ.get("OPENROUTER_KEY", ""),
        "groq": os.environ.get("GROQ_KEY", ""),
    }
    key = keys.get(provider, "")
    if not key or "tu_clave" in key:
        raise ValueError(f"❌ La clave para {provider} no está configurada en .env")
    return key
