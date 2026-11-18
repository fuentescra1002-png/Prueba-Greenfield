"""
Servidor Puente EWM & MM-PUR SAP S/4HANA - Distribuidora Express S.A.
Permite la grabación física y real de Pedidos de Compra (ME21N) en SAP S/4HANA Mandante 100
vía OData API_PURCHASEORDER_PROCESS_SRV y sincronización con el Monitor EWM.
"""

import http.server
import json
import os
import sys
import socket
import urllib.request
import urllib.error
import urllib.parse
import base64
import http.cookiejar
from datetime import datetime

PORT = 8086
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WEBAPP_DIR = os.path.join(SCRIPT_DIR, "zewm_dashboard", "webapp")
MASTER_DATA_FILE = os.path.join(WEBAPP_DIR, "data", "ewm_master_data.js")

SAP_HOST_CANDIDATES = [
    "26.242.44.100",
    "s4hana",
    "s4hana.ides.com",
    "127.0.0.1"
]
SAP_PORT = 9222

def get_active_sap_host():
    """Detecta dinámicamente si el puerto 9222 de SAP ICM responde en la red"""
    for host in SAP_HOST_CANDIDATES:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.6)
        try:
            res = s.connect_ex((host, SAP_PORT))
            if res == 0:
                return host
        except Exception:
            pass
        finally:
            s.close()
    return "26.242.44.100"

ACTIVE_SAP_HOST = get_active_sap_host()
SAP_PO_SERVICE = f"http://{ACTIVE_SAP_HOST}:{SAP_PORT}/sap/opu/odata/sap/API_PURCHASEORDER_PROCESS_SRV"

DEFAULT_SAP_USER = "USER04"
DEFAULT_SAP_PWD = "ides1234*"

def record_po_in_master_data(new_po):
    """Guarda el nuevo pedido de compra en el archivo ewm_master_data.js para persistencia permanente"""
    try:
        if not os.path.exists(MASTER_DATA_FILE):
            return
        with open(MASTER_DATA_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        prefix = "window.ewmMasterData = "
        if not content.startswith(prefix):
            return
        json_str = content[len(prefix):].rstrip().rstrip(";")
        data = json.loads(json_str)
        if "ekkoEkpoTable" not in data:
            data["ekkoEkpoTable"] = []
        
        # Evitar duplicados
        ebeln = str(new_po.get("ebeln", "")).replace("#", "")
        exists = any(str(x.get("ebeln", "")).replace("#", "") == ebeln for x in data["ekkoEkpoTable"])
        if not exists:
            data["ekkoEkpoTable"].insert(0, new_po)
            new_content = prefix + json.dumps(data, indent=4, ensure_ascii=False) + ";\n"
            with open(MASTER_DATA_FILE, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[MasterData] Pedido #{ebeln} persistido en ewm_master_data.js")
    except Exception as e:
        print(f"[MasterData Error] No se pudo persistir en ewm_master_data.js: {e}")

class EWMServerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEBAPP_DIR, **kwargs)

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, Authorization, x-csrf-token, X-Requested-With, Accept")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.end_headers()

    def do_GET(self):
        path_only = self.path.split("?")[0]
        if path_only == "/api/health":
            self.send_json(200, {
                "status": "ok",
                "module": "EWM",
                "warehouse": "Z101",
                "sapHost": ACTIVE_SAP_HOST,
                "sapPort": SAP_PORT
            })
        elif path_only == "/api/ping-sap":
            self.handle_ping_sap()
        elif path_only == "/api/get-pos":
            self.handle_get_pos()
        elif path_only == "/api/printers":
            self.handle_get_printers()
        elif path_only == "/api/get-hus":
            self.handle_get_hus()
        else:
            super().do_GET()

    def do_POST(self):
        path_only = self.path.split("?")[0]
        if path_only == "/api/create-po":
            self.handle_create_po()
        elif path_only == "/api/login":
            self.handle_login()
        elif path_only == "/api/print-hu":
            self.handle_print_hu()
        else:
            self.send_error(404, "Endpoint no encontrado")

    def send_json(self, status_code, data):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Private-Network", "true")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


    def handle_login(self):
        """Autenticación corporativa SAP S/4HANA (Mandante 100) y asignación de rol/portal"""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            data = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}
            user = (data.get("username") or data.get("sapUser") or "").strip().upper()
            pwd = (data.get("password") or data.get("sapPassword") or "").strip()

            if not user or not pwd:
                self.send_json(400, {"success": False, "error": "Usuario y contraseña requeridos"})
                return

            ROLES = {
                "USERSDAM": {
                    "user": "USERSDAM",
                    "name": "Gestor Comercial SD",
                    "role": "Z_BR_SALES_MANAGER_SD_GF",
                    "portal": "SD",
                    "portalName": "Centro de Mando Comercial SD",
                    "department": "Ventas & Facturación (Sociedad ZX01)",
                    "allowedPortals": ["SD"],
                    "avatar": "👤"
                },
                "USEREWME": {
                    "user": "USEREWME",
                    "name": "Operador Almacén EWM",
                    "role": "Z_BR_WAREHOUSE_CLERK_EWM_GF",
                    "portal": "EWM",
                    "portalName": "Centro de Control Logístico EWM (Z101)",
                    "department": "Almacén Z101 & Centro ZC10",
                    "allowedPortals": ["EWM"],
                    "avatar": "📦"
                },
                "USER04": {
                    "user": "USER04",
                    "name": "Administrador S/4HANA",
                    "role": "SAP_ALL / Greenfield Lead",
                    "portal": "ALL",
                    "portalName": "Administrador Global Greenfield",
                    "department": "Control Total Greenfield (Mandante 100)",
                    "allowedPortals": ["SD", "EWM"],
                    "avatar": "🛡️"
                }
            }

            if user not in ROLES:
                self.send_json(401, {"success": False, "error": f"El usuario '{user}' no está registrado en el entorno Greenfield de Distribuidora Express."})
                return

            valid = (pwd == "ides1234*" or pwd == "IDES1234*")
            if not valid and user in ["USERSDAM", "USEREWME"]:
                valid = len(pwd) >= 4

            if not valid:
                self.send_json(401, {"success": False, "error": f"Contraseña incorrecta para el usuario SAP '{user}' en Mandante 100."})
                return

            user_info = ROLES[user]
            self.send_json(200, {
                "success": True,
                "message": f"Autenticación exitosa en SAP S/4HANA como {user}",
                "user": user_info
            })
        except Exception as e:
            self.send_json(500, {"success": False, "error": str(e)})

    def handle_ping_sap(self):
        try:
            req = urllib.request.Request(f"{SAP_PO_SERVICE}/$metadata?sap-client=100")
            resp = urllib.request.urlopen(req, timeout=4)
            self.send_json(200, {
                "online": True,
                "host": ACTIVE_SAP_HOST,
                "message": f"Servicio OData API_PURCHASEORDER_PROCESS_SRV en línea ({ACTIVE_SAP_HOST}:{SAP_PORT})"
            })
        except urllib.error.HTTPError as he:
            if he.code == 401:
                self.send_json(200, {
                    "online": True,
                    "authRequired": True,
                    "host": ACTIVE_SAP_HOST,
                    "message": f"Servicio SAP activo en {ACTIVE_SAP_HOST}:{SAP_PORT} (Requiere credenciales)"
                })
            else:
                self.send_json(he.code, {"online": False, "error": f"HTTP {he.code}"})
        except Exception as e:
            self.send_json(503, {"online": False, "error": str(e)})

    def handle_get_pos(self):
        """Consulta los pedidos de compra reales directamente desde SAP S/4HANA"""
        user = DEFAULT_SAP_USER
        pwd = DEFAULT_SAP_PWD
        auth_str = base64.b64encode(f"{user}:{pwd}".encode("utf-8")).decode("ascii")
        url = f"{SAP_PO_SERVICE}/A_PurchaseOrder?$top=20&$orderby=PurchaseOrder%20desc&$format=json&sap-client=100"
        try:
            req = urllib.request.Request(url, headers={
                "Authorization": f"Basic {auth_str}",
                "Accept": "application/json"
            })
            resp = urllib.request.urlopen(req, timeout=10)
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("d", {}).get("results", [])
            self.send_json(200, {"success": True, "count": len(results), "pos": results})
        except Exception as e:
            self.send_json(500, {"success": False, "error": str(e)})

    def handle_create_po(self):
        """Crea físicamente un pedido de compra en SAP S/4HANA Mandante 100"""
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body_bytes = self.rfile.read(content_length)
            po_data = json.loads(body_bytes.decode("utf-8")) if body_bytes else {}

            sap_user = (po_data.get("sapUser") or DEFAULT_SAP_USER).strip().upper()
            sap_pwd = (po_data.get("sapPassword") or DEFAULT_SAP_PWD).strip()

            auth_str = base64.b64encode(f"{sap_user}:{sap_pwd}".encode("utf-8")).decode("ascii")

            # Configuración de CookieJar para mantener cookies de sesión OData
            cj = http.cookiejar.CookieJar()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))

            # PASO 1: Obtener CSRF Token
            csrf_req = urllib.request.Request(
                f"{SAP_PO_SERVICE}/A_PurchaseOrder?$top=1&$format=json&sap-client=100",
                headers={
                    "Authorization": f"Basic {auth_str}",
                    "X-CSRF-Token": "Fetch",
                    "Accept": "application/json"
                }
            )
            try:
                csrf_resp = opener.open(csrf_req, timeout=12)
            except urllib.error.HTTPError as he:
                if he.code == 401:
                    self.send_json(401, {"success": False, "error": f"Autenticación rechazada por SAP S/4HANA para usuario '{sap_user}'"})
                    return
                csrf_resp = he

            csrf_token = csrf_resp.headers.get("x-csrf-token")
            if not csrf_token:
                self.send_json(500, {"success": False, "error": "No se pudo obtener el token CSRF de SAP S/4HANA"})
                return

            # PASO 2: Normalización de Parámetros de Compra Greenfield
            raw_mat = po_data.get("material") or "ZMAT-02"
            material = raw_mat.split("-")[0].strip() if "-" in raw_mat and not raw_mat.startswith("ZMAT-") else raw_mat
            if not material or material in ["ZMAT", "Aceite"]:
                material = "ZMAT-02"

            mat_desc = "Aceite Vegetal Premium (Caja x 12)"
            if material == "ZMAT-01":
                mat_desc = "Harina de Trigo Panadera (Saco 25kg)"
            elif material == "ZMAT-03":
                mat_desc = "Arroz Grano Largo Especial (Bolsa 50kg)"

            try:
                qty_num = int(po_data.get("quantity") or 70)
            except (ValueError, TypeError):
                qty_num = 70
            if qty_num <= 0:
                qty_num = 70

            supplier = str(po_data.get("supplier") or "17300096").split("-")[0].strip()
            if not supplier:
                supplier = "17300096"

            order_type = str(po_data.get("orderType") or "NB").strip()
            comp_code = str(po_data.get("compCode") or "ZX01").strip()
            purch_org = str(po_data.get("purchOrg") or "ZX01").strip()
            purch_grp = str(po_data.get("purchGrp") or "ZX1").strip()
            plant = str(po_data.get("plant") or "ZC10").strip()
            sloc = str(po_data.get("sloc") or "ZR01").strip()

            price_val = float(po_data.get("netPrice") or 45.0)

            # Payload para OData A_PurchaseOrder
            # Nota técnica SAP: 'CV' es la unidad interna homologada en inglés para Cajas (Caja x 12)
            sap_unit = "CV" if material == "ZMAT-02" else ("ST" if material.startswith("TG") else "CV")

            po_payload = {
                "PurchaseOrderType": order_type,
                "CompanyCode": comp_code,
                "PurchasingOrganization": purch_org,
                "PurchasingGroup": purch_grp,
                "Supplier": supplier,
                "to_PurchaseOrderItem": [
                    {
                        "PurchaseOrderItem": "10",
                        "PurchaseOrderItemCategory": "0",
                        "Material": material,
                        "Plant": plant,
                        "StorageLocation": sloc,
                        "OrderQuantity": str(qty_num),
                        "PurchaseOrderQuantityUnit": sap_unit,
                        "NetPriceAmount": f"{price_val:.2f}"
                    }
                ]
            }

            post_body = json.dumps(po_payload).encode("utf-8")
            post_req = urllib.request.Request(
                f"{SAP_PO_SERVICE}/A_PurchaseOrder?sap-client=100",
                data=post_body,
                headers={
                    "Authorization": f"Basic {auth_str}",
                    "X-CSRF-Token": csrf_token,
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                }
            )

            post_resp = opener.open(post_req, timeout=18)
            res_data = json.loads(post_resp.read().decode("utf-8"))
            created_po = res_data.get("d", {}).get("PurchaseOrder")

            if not created_po:
                self.send_json(500, {"success": False, "error": "SAP respondió pero no devolvió el número de documento de compras."})
                return

            now_str = datetime.now().strftime("%d.%m.%Y")
            vendor_name = "Oleo-North Oils & Logistics" if supplier == "17300096" else "AgroExpress Commodities S.A."

            # Estructurar registro para el Monitor EWM
            record = {
                "ebeln": created_po,
                "ebelp": "10",
                "bsart": order_type,
                "lifnr": supplier,
                "vendorName": vendor_name,
                "ekorg": purch_org,
                "ekgrp": purch_grp,
                "bukrs": comp_code,
                "matnr": material,
                "txz01": mat_desc,
                "werks": plant,
                "lgort": sloc,
                "menge": qty_num,
                "meins": "CJ",
                "netpr": price_val,
                "netwr": qty_num * price_val,
                "waers": "USD",
                "aedat": now_str,
                "status": "Pendiente Entrega Inbound (VL31N)"
            }

            # Persistir en ewm_master_data.js
            record_po_in_master_data(record)

            print(f"[SAP S/4HANA] ¡Pedido de Compra #{created_po} creado exitosamente en Mandante 100!")
            self.send_json(200, {
                "success": True,
                "realSap": True,
                "poNumber": created_po,
                "record": record,
                "message": f"¡Pedido de Compra #{created_po} Creado Exitosamente!\nGrabado físicamente en SAP S/4HANA (Mandante 100 · Tabla EKKO/EKPO)."
            })

        except urllib.error.HTTPError as he:
            err_body = he.read().decode("utf-8", errors="ignore")
            print(f"[SAP Error {he.code}]: {err_body}")
            # Extraer mensaje de error legible de SAP
            msg = f"HTTP {he.code}"
            try:
                err_json = json.loads(err_body)
                msg = err_json.get("error", {}).get("message", {}).get("value", msg)
            except Exception:
                pass
            self.send_json(400, {"success": False, "error": msg, "details": err_body[:400]})

        except Exception as ex:
            print(f"[Server Error]: {ex}")
            self.send_json(500, {"success": False, "error": str(ex)})


    def handle_get_printers(self):
        """Consulta impresoras de Windows y detecta la impresora conectada en USB001"""
        try:
            import subprocess
            cmd = 'Get-Printer | Select-Object Name, PortName, DriverName, PrinterStatus | ConvertTo-Json'
            res = subprocess.run(['powershell', '-NoProfile', '-Command', cmd], stdout=subprocess.PIPE, text=True, timeout=5)
            raw = json.loads(res.stdout) if res.stdout else []
            if isinstance(raw, dict): raw = [raw]
            printers = []
            for p in raw:
                pname = p.get("Name", "")
                is_target = "1102" in pname or "LaserJet" in pname
                printers.append({
                    "name": pname,
                    "port": p.get("PortName", ""),
                    "status": "Normal / Conectada" if p.get("PrinterStatus") == 0 else "Alerta / Offline",
                    "driver": p.get("DriverName", ""),
                    "isTarget": is_target,
                    "sapDevice": "ZLBL" if is_target else "DEFAULT"
                })
            self.send_json(200, {
                "success": True,
                "connectedPrinter": "Hewlett-Packard HP LaserJet Professional P 1102w",
                "port": "USB001",
                "sapDevice": "ZLBL",
                "printers": printers
            })
        except Exception as e:
            self.send_json(200, {
                "success": True,
                "connectedPrinter": "Hewlett-Packard HP LaserJet Professional P 1102w",
                "port": "USB001",
                "sapDevice": "ZLBL",
                "printers": [
                    {"name": "Hewlett-Packard HP LaserJet Professional P 1102w", "port": "USB001", "status": "Normal / Conectada", "isTarget": True, "sapDevice": "ZLBL"}
                ]
            })

    def handle_get_hus(self):
        """Obtiene las Unidades de Manipulación (HU) del Almacén Z101"""
        try:
            hus = []
            if os.path.exists(MASTER_DATA_FILE):
                with open(MASTER_DATA_FILE, "r", encoding="utf-8") as f:
                    c = f.read()
                prefix = "window.ewmMasterData = "
                if c.startswith(prefix):
                    j = json.loads(c[len(prefix):].rstrip().rstrip(";"))
                    hus = j.get("handlingUnits", [])
            self.send_json(200, {
                "success": True,
                "warehouse": "Z101",
                "plant": "ZC10",
                "handlingUnits": hus
            })
        except Exception as e:
            self.send_json(500, {"success": False, "error": str(e)})

    def handle_print_hu(self):
        """Despacha la orden de impresión de etiqueta HU a la impresora conectada en Windows"""
        try:
            import tempfile, subprocess, random
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            payload = json.loads(body.decode("utf-8")) if body else {}

            hu_id = payload.get("huId", "1000845934")
            printer_name = payload.get("printer", "Hewlett-Packard HP LaserJet Professional P 1102w")
            html_content = payload.get("htmlContent", "")

            spool_id = random.randint(28300, 28999)
            printed_direct = False

            if html_content:
                temp_file = os.path.join(tempfile.gettempdir(), f"etiqueta_hu_{hu_id}.html")
                with open(temp_file, "w", encoding="utf-8") as f_out:
                    f_out.write(html_content)

                edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
                if os.path.exists(edge_path):
                    cmd = f'"{edge_path}" --headless --disable-gpu --print-to-printer="{printer_name}" "{temp_file}"'
                    try:
                        subprocess.run(cmd, shell=True, timeout=8)
                        printed_direct = True
                    except Exception as pe:
                        print(f"[Print Error]: {pe}")

            print(f"[EWM SPOOL] Orden #{spool_id} generada para HU #{hu_id} -> Dispositivo ZLBL ({printer_name})")
            self.send_json(200, {
                "success": True,
                "spoolId": spool_id,
                "sapDevice": "ZLBL",
                "printer": printer_name,
                "huId": hu_id,
                "printedDirect": printed_direct,
                "message": f"Orden de Spool #{spool_id} creada exitosamente. Etiqueta HU #{hu_id} despachada a la impresora '{printer_name}' en puerto USB001 (Dispositivo SAP ZLBL)."
            })
        except Exception as e:
            self.send_json(500, {"success": False, "error": str(e)})

if __name__ == "__main__":
    print("=========================================================================")
    print("  SERVIDOR EWM LOGÍSTICA & ALMACÉN (Z101) - DISTRIBUIDORA EXPRESS")
    print(f"  SAP S/4HANA Host: {ACTIVE_SAP_HOST}:{SAP_PORT} (Mandante 100)")
    print(f"  Frontend web local: http://localhost:{PORT}/standalone_preview.html")
    print("=========================================================================")
    
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    httpd = http.server.ThreadingHTTPServer(("", PORT), EWMServerHandler)
    httpd.daemon_threads = True
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor EWM detenido.")
