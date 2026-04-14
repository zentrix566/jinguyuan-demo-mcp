#!/usr/bin/env python3
import requests

url = "http://localhost:8000/mcp"
data = {
    "name": "get_wifi_password",
    "parameters": {
        "question": "WiFi密码是多少"
    }
}

response = requests.post(url, json=data)
print(response.json())
