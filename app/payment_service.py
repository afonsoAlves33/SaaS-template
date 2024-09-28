import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

token = os.getenv("token")

url = url = "https://sandbox.asaas.com/api/v3/myAccount/commercialInfo/"

headers = {"access_token": token}

response = requests.get(url, headers=headers).json()

beautiful_resp =  json.dumps(response, indent=4)

print(beautiful_resp)