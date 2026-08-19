import requests
import base64

# Read and encode your audio file
with open("data\\WhatsApp Ptt 2026-08-19 at 1.13.33 PM.wav", "rb") as f:
    audio_base64 = base64.b64encode(f.read()).decode()

url = "https://api.tryhamsa.com/v1/realtime/stt"
headers = {
    "Authorization": "Token 85d1acc7-b93b-425a-8c9e-3e2900281246",
    "Content-Type": "application/json"
}
data = {
    "audioBase64": audio_base64,
    "language": "ar",
    "model": "s2"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
# Returns: { "text": "مرحبا بك في خدمة همسة" }