import requests

url = "https://api.tryhamsa.com/v1/jobs/transcribe"
headers = {
    "Authorization": "Token 85d1acc7-b93b-425a-8c9e-3e2900281246",
    "Content-Type": "application/json"
}
data = {
    "mediaUrl": "https://raw.githubusercontent.com/Cat5TV/audiotest/refs/heads/master/test.mp3",
    "model": "Hamsa-General-V2.0",
    "language": "en"
}

response = requests.post(url, headers=headers, json=data)
print(response.json())
# Returns: { "success": true, "data": { "jobId": "..." } }