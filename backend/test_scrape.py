import requests

url = "https://freshershunt.in/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}
response = requests.get(url, headers=headers)
with open('page.html', 'w', encoding='utf-8') as f:
    f.write(response.text)
