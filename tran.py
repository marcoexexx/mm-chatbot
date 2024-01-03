import requests

url = "https://google-translate1.p.rapidapi.com/language/translate/v2"

payload = {
	"source": "en",
	"target": "es",
	"q": "Hello, world!"
}
headers = {
	"content-type": "application/x-www-form-urlencoded",
	"Accept-Encoding": "application/gzip",
	"X-RapidAPI-Key": "f2a73db4damsh5eeaec6e4d25f09p1dde6djsnbfeb7ab3bc3f",
	"X-RapidAPI-Host": "google-translate1.p.rapidapi.com"
}

response = requests.post(url, data=payload, headers=headers)

print(response.json())
