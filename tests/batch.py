import requests

url = "https://api.tryhamsa.com/v1/jobs/transcribe"
headers = {
    "Authorization": "Bearer YOUR_API_KEY",
    "Content-Type": "application/json"
}
data = {
    "mediaUrl": "https://your-storage.com/audio.mp3",
    "model": "Hamsa-General-V2.0",
    "language": "ar",
    "webhookUrl": "https://your-server.com/webhook"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
# Returns: { "success": true, "data": { "jobId": "..." } }