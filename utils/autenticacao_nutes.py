import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.nutespb.com.br/v1/auth"
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/json'
}
data = {
    'login': 'admin@ssm.com',
    'password': 'admin123'
}

resp = requests.post(url, headers=headers, json=data)
token = resp.json()['access_token']
