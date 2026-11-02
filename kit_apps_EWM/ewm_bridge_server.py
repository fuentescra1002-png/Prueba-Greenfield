import http.server
import json
import os
import sys

PORT = 8086
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WEBAPP_DIR = os.path.join(SCRIPT_DIR, "zewm_dashboard", "webapp")

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
            self.send_json(200, {"status": "ok", "module": "EWM", "warehouse": "Z101"})
        else:
            super().do_GET()

    def send_json(self, status_code, data):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

if __name__ == "__main__":
    print("=========================================================================")
    print("  SERVIDOR EWM LOGÍSTICA & ALMACÉN (Z101) - DISTRIBUIDORA EXPRESS")
    print(f"  Frontend web local: http://localhost:{PORT}/standalone_preview.html")
    print("=========================================================================")
    
    http.server.ThreadingHTTPServer.allow_reuse_address = True
    httpd = http.server.ThreadingHTTPServer(("", PORT), EWMServerHandler)
    httpd.daemon_threads = True
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor EWM detenido.")
