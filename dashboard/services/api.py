import requests

API_URL = "http://localhost:8000"

def get_produtos(token):
    headers = {"Authorization": f"Bearer {token}"}
    return requests.get(f"{API_URL}/produtos", headers=headers).json()