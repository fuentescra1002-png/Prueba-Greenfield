import urllib.request, urllib.parse, re, http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

url = 'http://26.242.44.100:9222/sap/bc/gui/sap/its/webgui?sap-client=100'
resp = opener.open(url, timeout=5)
html = resp.read().decode('utf-8', errors='ignore')

xsrf_match = re.search(r'name=\"sap-login-XSRF\"\s+value=\"([^\"]+)\"', html)
xsrf = xsrf_match.group(1) if xsrf_match else ''

post_data = urllib.parse.urlencode({
    'sap-system-login': 'onLogin',
    'sap-system-login-oninputprocessing': 'onLogin',
    'sap-login-XSRF': xsrf,
    'sap-client': '100',
    'sap-user': 'USER04',
    'sap-password': 'ides1234*',
    'sap-language': 'ES'
}).encode('utf-8')

post_url = 'http://26.242.44.100:9222/sap/bc/gui/sap/its/webgui'
req = urllib.request.Request(post_url, data=post_data)
post_resp = opener.open(req, timeout=8)
post_html = post_resp.read().decode('utf-8', errors='ignore')

# Print lines containing any text
clean = re.sub(r'<[^>]+>', '\n', post_html)
lines = [l.strip() for l in clean.splitlines() if l.strip() and len(l.strip()) > 3]
print('\n'.join(lines[10:40]))
