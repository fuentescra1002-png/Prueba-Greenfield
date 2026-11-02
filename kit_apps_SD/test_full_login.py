import urllib.request, urllib.parse, re, http.cookiejar

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

# 1. GET page to get XSRF and cookies
url = 'http://26.242.44.100:9222/sap/bc/gui/sap/its/webgui?sap-client=100'
resp = opener.open(url, timeout=5)
html = resp.read().decode('utf-8', errors='ignore')

xsrf_match = re.search(r'name=\"sap-login-XSRF\"\s+value=\"([^\"]+)\"', html)
xsrf = xsrf_match.group(1) if xsrf_match else ''
print('XSRF token:', xsrf)

# 2. POST login form
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
try:
    post_resp = opener.open(req, timeout=8)
    print('POST Status:', post_resp.status)
    print('Final URL after login:', post_resp.geturl())
    print('Cookies after login:')
    for c in cj:
        print(f'  {c.name} = {c.value[:30]}...')
    post_html = post_resp.read().decode('utf-8', errors='ignore')
    print('Logged in title/head:', re.findall(r'<title>(.*?)</title>', post_html, re.I))
    if 'LOGONREQUIRED' in post_html or 'Anmeldung' in post_html:
        print('Still at logon screen')
        # check message
        err_m = re.findall(r'class=\"[^\"]*message[^\"]*\"[^>]*>(.*?)<', post_html, re.I)
        print('Error message:', err_m)
    else:
        print('SUCCESSFULLY LOGGED IN TO SAP!')
except urllib.error.HTTPError as e:
    print('HTTP ERROR on login:', e.code)
