import sys
import os

# Aggiungi il path principale
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Scuola, Sensore
import random

def seed_pressure_sensors():
    db = SessionLocal()
    scuole = db.query(Scuola).all()
    
    added = 0
    for scuola in scuole:
        # Check if a pressure sensor already exists
        p_sensor = db.query(Sensore).filter(Sensore.scuola_id == scuola.id, Sensore.tipo == "Pressione").first()
        if not p_sensor:
            # Generate a unique topic
            topic = f"tesi/catania/scuole/{scuola.id}/pressione_{random.randint(1000, 9999)}"
            nuovo_sensore = Sensore(
                scuola_id=scuola.id,
                nome="Sensore Pressione Rete",
                is_main=False,
                tipo="Pressione",
                topic_mqtt=topic
            )
            db.add(nuovo_sensore)
            added += 1
            
    if added > 0:
        db.commit()
        print(f"Aggiunti {added} sensori di pressione nel database.")
    else:
        print("Tutte le scuole hanno già un sensore di pressione.")
        
    db.close()

if __name__ == "__main__":
    seed_pressure_sensors()
