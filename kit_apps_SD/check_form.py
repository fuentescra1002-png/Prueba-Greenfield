import urllib.request, urllib.parse, re, http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. GET page to get XSRF
url = 'http://26.242.44.100:9222/sap/bc/gui/sap/its/webgui?sap-client=100'
resp = opener.open(url, timeout=5)
html = resp.read().decode('utf-8', errors='ignore')
xsrf_m = re.search(r'name="sap-login-XSRF"\s+value="([^"]+)"', html)
xsrf = xsrf_m.group(1) if xsrf_m else ''

post_data = urllib.parse.urlencode({
    'sap-system-login': 'onLogin',
    'sap-system-login-oninputprocessing': 'onLogin',
    'sap-login-XSRF': xsrf,
    'sap-client': '100',
    'sap-user': 'USERSDAM',
    'sap-password': 'ides1234*',
    'sap-language': 'ES'
}).encode('utf-8')

req = urllib.request.Request('http://26.242.44.100:9222/sap/bc/gui/sap/its/webgui', data=post_data)
resp = opener.open(req, timeout=5)
post_html = resp.read().decode('utf-8', errors='ignore')

# find messages or alerts in HTML
msg_matches = re.findall(r'class="[^"]*(?:message|error|alert)[^"]*"[^>]*>(.*?)<', post_html, re.I)
print('USERSDAM post status:', resp.status)
print('Messages:', msg_matches)

# Let's search for text near 'sap' or 'contraseña' or 'error'
clean_text = re.sub(r'<[^>]+>', ' ', post_html)
lines = [l.strip() for l in clean_text.splitlines() if l.strip()]
for l in lines:
    if any(k in l.lower() for k in ['error', 'incorrect', 'clave', 'contrase', 'bloquead', 'caduc', 'inicial', 'modifi', 'usuario', 'no existe']):
        print('  line:', l[:120])
