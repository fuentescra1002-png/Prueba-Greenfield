import urllib.request, re

url = 'http://26.242.44.100:9222/sap/bc/gui/sap/its/webgui?sap-client=100'
req = urllib.request.Request(url)
resp = urllib.request.urlopen(req, timeout=5)
cookies = resp.headers.get_all('set-cookie') or []
print('Initial cookies:', cookies)
html = resp.read().decode('utf-8', errors='ignore')

# Find form action and inputs
forms = re.findall(r'<form.*?</form>', html, re.DOTALL | re.I)
for f in forms:
    print('FORM:', f[:300])
    inputs = re.findall(r'<input[^>]+>', f, re.I)
    for inp in inputs:
        print('  INPUT:', inp)
