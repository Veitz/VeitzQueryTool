import requests

url = "https://api.onetrading.com/fast/v1/instruments?type=SPOT"
#url = "https://api.onetrading.com/fast/v1/instruments?type=PERPETUAL_FUTURES"

payload={}
headers = {
   'Authorization': 'Bearer <token>'
}

response = requests.request("GET", url, headers=headers, data=payload)

#print(response.text)
if response.status_code == 200:
    with open("instruments.json", "w", encoding="utf-8") as f:
        f.write(response.text)
    print("Gespeichert → instruments.json")
else:
    print(f"Fehler: {response.status_code} - {response.text[:200]}")
