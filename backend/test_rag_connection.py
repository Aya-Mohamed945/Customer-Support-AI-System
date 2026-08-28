# test_rag_connection.py
import requests

url = "http://127.0.0.1:8001/api/v1/rag/retrieve"
data = {"query": "refund", "k": 2, "threshold": 0.1}

try:
    response = requests.post(url, json=data, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")