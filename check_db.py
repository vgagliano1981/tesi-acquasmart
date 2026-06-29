import sqlite3

conn = sqlite3.connect('iot_platform.db')
cursor = conn.cursor()

cursor.execute('SELECT COUNT(*) FROM sensori WHERE tipo IN ("Torbidità", "Conducibilità")')
print("Sensori aggiunti:", cursor.fetchone()[0])

cursor.execute('SELECT COUNT(*) FROM letture JOIN sensori ON letture.sensore_id = sensori.id WHERE sensori.tipo IN ("Torbidità", "Conducibilità")')
print("Letture generate:", cursor.fetchone()[0])

conn.close()
