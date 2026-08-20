import requests

url = "https://api.tryhamsa.com/v1/jobs/transcribe"
headers = {
    "Authorization": "Token 85d1acc7-b93b-425a-8c9e-3e2900281246",
    "Content-Type": "application/json"
}
data = {
    "mediaUrl": "https://raw.githubusercontent.com/saleh1312/stt_tts_youtube_scrap/refs/heads/main/data/WhatsApp Ptt 2026-08-19 at 1.13.33 PM.wav",
    "model": "Hamsa-General-V2.0",
    "language": "ar"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
# Returns: { "success": true, "data": { "jobId": "..." } }