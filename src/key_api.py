import os

api_key = os.getenv("API_KEY")
if api_key:
    print(f"API Key configurada: {api_key}")
else:
    print("API Key não configurada!")
    

