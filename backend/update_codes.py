import sqlite3

# Mapping school names to actual "Codice Meccanografico" from unica.istruzione
codes_mapping = {
    "Liceo Scientifico G. Galilei": "CTPS040009",
    "Liceo Classico N. Spedalieri": "CTPC070002",
    "Liceo Classico M. Cutelli": "CTVC01000N",
    "Liceo Scientifico E. Boggio Lera": "CTPS020004",
    "I.T.I.S. Archimede": "CTTF01000G",
    "I.I.S. G.B. Vaccarini": "CTIS01700V",
    "I.T. Aeronautico A. Ferrarin": "CTTB01000A",
    "Liceo Statale G. Lombardo Radice": "CTPM03000Q",
    "I.I.S.S. Carlo Gemmellaro": "CTIS023006",
    "Liceo Artistico Statale M.M. Lazzaro": "CTSD02000E"
}

conn = sqlite3.connect('iot_platform.db')
cursor = conn.cursor()

for name, code in codes_mapping.items():
    cursor.execute('''
        UPDATE scuole
        SET codice_meccanografico = ?
        WHERE nome = ?
    ''', (code, name))

conn.commit()
conn.close()

print("Codici meccanografici aggiornati con successo.")
