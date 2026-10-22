import os
import requests

# Leer la clave de la variable de entorno
api_key = os.environ.get("LER_API_KEY", "")

if not api_key:
    print("❌ No hay variable LER_API_KEY en el entorno.")
    print("Ejecutá: export LER_API_KEY='gsk_...'")
    exit(1)

print(f"Clave detectada (primeros 10 caracteres): {api_key[:10]}...")
print(f"Largo de la clave: {len(api_key)}")

# Hacer una petición cruda a Groq
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
data = {
    "model": "openai/gpt-oss-120b",
    "messages": [{"role": "user", "content": "Decime 'Hola' en una palabra."}],
    "temperature": 0.0
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=10)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        print("✅ ¡La API Key es válida!")
        print("Respuesta de Llama 3:", response.json()["choices"][0]["message"]["content"])
    else:
        print(f"❌ Error: {response.text}")
except Exception as e:
    print(f"❌ Error de conexión: {e}")
