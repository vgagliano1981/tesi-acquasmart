import urllib.request
url = "https://upload.wikimedia.org/wikipedia/it/a/a2/Citt%C3%A0_metropolitana_di_Catania-Stemma.svg"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'it-IT,it;q=0.9,en-US;q=0.8,en;q=0.7',
}
req = urllib.request.Request(url, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        data = response.read()
        with open('frontend/logo_catania.svg', 'wb') as f:
            f.write(data)
        print('Download Success')
except Exception as e:
    print('Download Failed:', e)
