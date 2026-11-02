import urllib.request, urllib.parse, re

url = 'http://26.242.44.100:9222/sap/bc/gui/sap/its/webgui?sap-client=100'
data = urllib.parse.urlencode({
    'sap-user': 'USER04',
    'sap-password': 'ides1234*',
    'sap-client': '100',
    'sap-language': 'ES'
}).encode('utf-8')

req = urllib.request.Request(url, data=data)
resp = urllib.request.urlopen(req, timeout=5)
body = resp.read().decode('utf-8', errors='ignore')

# Search for any error or message texts
clean_text = re.sub(r'<style.*?</style>', '', body, flags=re.DOTALL)
clean_text = re.sub(r'<script.*?</script>', '', clean_text, flags=re.DOTALL)
clean_text = re.sub(r'<[^>]+>', ' ', clean_text)
lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
print('\n'.join(lines[:30]))
