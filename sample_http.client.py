import http.client

conn = http.client.HTTPSConnection("api.onetrading.com")
payload = ''
headers = {
   'Authorization': 'Bearer <token>'
}
conn.request("GET", "/fast/v1/instruments?type=SPOT", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
with open("SPOT_instruments.json", "w", encoding="utf-8") as f:
   f.write(data.decode("utf-8"))