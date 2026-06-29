import sqlite3

def populate_sensors():
    conn = sqlite3.connect('iot_platform.db')
    cursor = conn.cursor()

    # Get all schools
    cursor.execute('SELECT id, nome FROM scuole')
    scuole = cursor.fetchall()

    for scuola_id, nome in scuole:
        # Check if a sensor already exists for this school
        cursor.execute('SELECT id FROM sensori WHERE scuola_id = ?', (scuola_id,))
        if not cursor.fetchone():
            topic = f"tesi/catania/scuole/{scuola_id}/sensore_acqua"
            cursor.execute('''
                INSERT INTO sensori (scuola_id, tipo, topic_mqtt)
                VALUES (?, 'Acqua', ?)
            ''', (scuola_id, topic))
            print(f"Creato sensore per {nome} con topic: {topic}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    populate_sensors()
