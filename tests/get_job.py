import requests

url = "https://api.tryhamsa.com/v1/jobs?jobId=4be92a83-afc7-4804-9696-8301f56498b1"

headers = {"Authorization": "Token 85d1acc7-b93b-425a-8c9e-3e2900281246"}

response = requests.get(url, headers=headers)

print(response.text)