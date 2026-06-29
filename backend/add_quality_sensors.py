import sys
import os

# Aggiungi il path principale
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Scuola, Sensore
import random

def seed_quality_sensors():
    db = SessionLocal()
    scuole = db.query(Scuola).all()
    
    added_t = 0
    added_c = 0
    
    for scuola in scuole:
        # Check Torbidità
        t_sensor = db.query(Sensore).filter(Sensore.scuola_id == scuola.id, Sensore.tipo == "Torbidità").first()
        if not t_sensor:
            topic_t = f"tesi/catania/scuole/{scuola.id}/torbidita_{random.randint(1000, 9999)}"
            s_torbidita = Sensore(
                scuola_id=scuola.id,
                nome="Sensore Torbidità",
                is_main=False,
                tipo="Torbidità",
                topic_mqtt=topic_t
            )
            db.add(s_torbidita)
            added_t += 1
            
        # Check Conducibilità
        c_sensor = db.query(Sensore).filter(Sensore.scuola_id == scuola.id, Sensore.tipo == "Conducibilità").first()
        if not c_sensor:
            topic_c = f"tesi/catania/scuole/{scuola.id}/conducibilita_{random.randint(1000, 9999)}"
            s_cond = Sensore(
                scuola_id=scuola.id,
                nome="Sensore Conducibilità",
                is_main=False,
                tipo="Conducibilità",
                topic_mqtt=topic_c
            )
            db.add(s_cond)
            added_c += 1
            
    if added_t > 0 or added_c > 0:
        db.commit()
        print(f"Aggiunti {added_t} sensori di torbidità e {added_c} sensori di conducibilità nel database.")
    else:
        print("Tutte le scuole hanno già i sensori di torbidità e conducibilità.")
        
    db.close()

if __name__ == "__main__":
    seed_quality_sensors()
