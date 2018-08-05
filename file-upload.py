import requests

url = "https://www.djvu-pdf.com/"
payload = {'q':'python'}
r = requests.post(url, payload)
with open("requests_results.html", "w") as f:
    f.write(r.content)