import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Scuola, Sensore

db = SessionLocal()

# Lista delle principali scuole superiori di Catania
scuole = [
    ("Liceo Scientifico G. Galilei", "Via Vescovo Maurizio, 73, Catania", 1200, "CTPS01000A"),
    ("Liceo Classico N. Spedalieri", "Piazza Annibale Riccò, Catania", 950, "CTPC01000A"),
    ("Liceo Classico M. Cutelli", "Via Firenze, 202, Catania", 1100, "CTPC02000B"),
    ("I.T.I.S. Archimede", "Viale Regina Margherita, 22, Catania", 1500, "CTTF01000D"),
    ("I.I.S. G.B. Vaccarini", "Via Orchidea, 9, Catania", 850, "CTIS01000A"),
    ("Liceo Scientifico E. Boggio Lera", "Via Vittorio Emanuele II, 346, Catania", 1300, "CTPS03000C"),
    ("I.T. Aeronautico A. Ferrarin", "Via Passo Gravina, 197, Catania", 700, "CTTA01000E"),
    ("Liceo Statale G. Lombardo Radice", "Via Imperia, 21, Catania", 1050, "CTPM01000G"),
    ("I.I.S.S. Carlo Gemmellaro", "Corso Indipendenza, 229, Catania", 900, "CTIS02000B"),
    ("Liceo Artistico Statale M.M. Lazzaro", "Via G. D'Annunzio, 113, Catania", 800, "CTSD01000F")
]

# Inserimento nel database
for index, (nome, indirizzo, studenti, cod_mecc) in enumerate(scuole):
    scuola_id = index + 1
    if not db.query(Scuola).filter(Scuola.id == scuola_id).first():
        s = Scuola(id=scuola_id, nome=nome, indirizzo=indirizzo, numero_studenti=studenti, codice_meccanografico=cod_mecc)
        db.add(s)
    
    # Contatore Principale
    topic_main = f'tesi/catania/scuole/{scuola_id}/sensore_acqua_main'
    if not db.query(Sensore).filter(Sensore.topic_mqtt == topic_main).first():
        s_main = Sensore(scuola_id=scuola_id, tipo='Acqua', topic_mqtt=topic_main, nome='Contatore Principale', is_main=True)
        db.add(s_main)
    
    # Sotto-sensori fittizi
    sotto_sensori = ["Bagni Studenti PT", "Vasca Antincendio", "Palestra e Docce"]
    for i, sn in enumerate(sotto_sensori):
        topic_sub = f'tesi/catania/scuole/{scuola_id}/sub_{i+1}'
        if not db.query(Sensore).filter(Sensore.topic_mqtt == topic_sub).first():
            s_sub = Sensore(scuola_id=scuola_id, tipo='Acqua', topic_mqtt=topic_sub, nome=sn, is_main=False)
            db.add(s_sub)

db.commit()
db.close()

print("Scuole e Sensori di Catania importati con successo nel database SQLAlchemy!")
