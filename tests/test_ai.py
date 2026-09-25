import requests

# Colocá tu clave directamente aquí
api_key = "9b8ae470e74248a1aa380395bf939c70.jbpWTe3VF3exv3BO"

# Endpoint de Zhipu
endpoint = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

payload = {
    "model": "glm-4",
    "messages": [
        {"role": "system", "content": "Eres una AI de prueba."},
        {"role": "user", "content": "Hola, ¿puedes responderme?"}
    ],
    "max_tokens": 100,
    "temperature": 0.1
}

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

try:
    response = requests.post(endpoint, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    print("✅ Respuesta de la AI:")
    print(data.get("choices", [{}])[0].get("message", {}).get("content", "Sin respuesta"))
except Exception as e:
    print("❌ Error de comunicación:", e)
