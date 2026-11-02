import sqlite3

conn = sqlite3.connect(r'C:\Users\Javier\AppData\Roaming\SAP\SAP GUI\History\SAPHistoryJAVIER.db')
c = conn.cursor()
c.execute("SELECT HistFieldname, HistTime, HistEntry FROM history WHERE HistFieldname LIKE '%BNAME%' OR HistFieldname LIKE '%USER%'")
for row in c.fetchall():
    print(row)
