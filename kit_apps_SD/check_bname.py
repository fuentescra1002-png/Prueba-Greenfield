import sqlite3

conn = sqlite3.connect(r'C:\Users\Javier\AppData\Roaming\SAP\SAP GUI\History\SAPHistoryJAVIER.db')
c = conn.cursor()
c.execute("SELECT Field, Key, Value FROM History WHERE Field LIKE '%BNAME%' OR Field LIKE '%UNAME%'")
for r in c.fetchall():
    print(r)
