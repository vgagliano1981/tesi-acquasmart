import os
import sys
import random
import numpy as np
from datetime import datetime, timedelta
from sklearn.ensemble import IsolationForest

# Aggiungi il path principale per i moduli interni
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal, engine
from backend.models import Sensore, Lettura, Base

# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

def _extract_features(value, timestamp):
    is_weekend = 1 if timestamp.weekday() >= 5 else 0
    is_night = 1 if timestamp.hour < 6 or timestamp.hour >= 20 else 0
    return [value, is_weekend, is_night]

def generate_historical_offline():
    db = SessionLocal()
    
    print("Pulizia delle letture precedenti...")
    db.query(Lettura).delete()
    db.commit()
    
    sensori_acqua = db.query(Sensore).filter(Sensore.tipo == "Acqua").all()
    if not sensori_acqua:
        print("Nessun sensore d'acqua trovato.")
        return

    scuole_sensori_acqua = {}
    for s in sensori_acqua:
        if s.scuola_id not in scuole_sensori_acqua:
            scuole_sensori_acqua[s.scuola_id] = {'main': None, 'subs': []}
        if s.is_main:
            scuole_sensori_acqua[s.scuola_id]['main'] = s
        else:
            scuole_sensori_acqua[s.scuola_id]['subs'].append(s)

    start_date = datetime.now() - timedelta(days=60)
    end_date = datetime.now()
    step_minutes = 10
    total_steps = int((end_date - start_date).total_seconds() / (step_minutes * 60))
    
    training_end_date = start_date + timedelta(days=14)
    
    print(f"Generazione dati storici OFFLINE SEPARATA per {total_steps} timestamp...")
    
    train_features = []
    all_readings = []
    
    current_time = start_date
    while current_time <= end_date:
        is_weekend = 1 if current_time.weekday() >= 5 else 0
        is_night = 1 if current_time.hour < 6 or current_time.hour >= 20 else 0
        is_training_phase = current_time <= training_end_date
        
        for scuola_id, sensori in scuole_sensori_acqua.items():
            main_sensor = sensori['main']
            sub_sensors = sensori['subs']
            sum_subs = 0.0
            
            for sub in sub_sensors:
                if is_night:
                    base_consumption = random.uniform(0.0, 0.2)
                elif is_weekend:
                    base_consumption = random.uniform(0.1, 0.5)
                else:
                    base_consumption = random.uniform(15.0, 20.0)
                
                valore = base_consumption
                is_anomaly = False
                anomaly_type = None
                
                if not is_training_phase and random.random() < 0.025:
                    if is_night or is_weekend:
                        valore += random.uniform(3.0, 8.0)
                        anomaly_type = "Anomalia Locale (Micro-perdita)"
                    else:
                        valore += random.uniform(15.0, 25.0)
                        anomaly_type = "Anomalia Locale (Perdita Maggiore)"
                    is_anomaly = True
                
                sum_subs += valore
                features = _extract_features(valore, current_time)
                
                if is_training_phase and len(train_features) < 20000:
                    train_features.append(features)
                    
                all_readings.append({
                    "sensore_id": sub.id,
                    "timestamp": current_time,
                    "valore_litri": round(valore, 2),
                    "is_ground_truth_anomaly": is_anomaly,
                    "ground_truth_type": anomaly_type,
                    "features": features
                })
            
            if main_sensor:
                main_valore = sum_subs
                is_anomaly = False
                anomaly_type = None
                
                if not is_training_phase and random.random() < 0.025:
                    perdita = random.uniform(25.0, 50.0) 
                    main_valore += perdita
                    is_anomaly = True
                    anomaly_type = "Perdita Occulta"
                    
                features = _extract_features(main_valore, current_time)
                
                if is_training_phase and len(train_features) < 20000:
                    train_features.append(features)
                    
                all_readings.append({
                    "sensore_id": main_sensor.id,
                    "timestamp": current_time,
                    "valore_litri": round(main_valore, 2),
                    "is_ground_truth_anomaly": is_anomaly,
                    "ground_truth_type": anomaly_type,
                    "features": features
                })
                
        current_time += timedelta(minutes=step_minutes)

    print(f"Addestramento OFFLINE del modello IsolationForest su {len(train_features)} campioni puliti...")
    # Usa esattamente la contamination usata in produzione (0.05) senza sbirciare nel test set
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(np.array(train_features))
    
    print("Predizione in bulk per tutta la cronologia...")
    X_all = np.array([r["features"] for r in all_readings])
    
    predictions = model.predict(X_all)
    scores = model.score_samples(X_all)
    
    print("Salvataggio nel database...")
    batch_size = 10000
    letture_objects = []
    
    for i, r in enumerate(all_readings):
        letture_objects.append(Lettura(
            sensore_id=r["sensore_id"],
            timestamp=r["timestamp"],
            valore_litri=r["valore_litri"],
            is_anomalia=bool(predictions[i] == -1),
            anomaly_score=float(scores[i]),
            is_ground_truth_anomaly=r["is_ground_truth_anomaly"],
            ground_truth_type=r["ground_truth_type"]
        ))
        
        if len(letture_objects) >= batch_size:
            db.bulk_save_objects(letture_objects)
            db.commit()
            letture_objects = []
            
    if letture_objects:
        db.bulk_save_objects(letture_objects)
        db.commit()

    print("Generazione ed elaborazione offline separata completata con successo!")
    db.close()

if __name__ == "__main__":
    generate_historical_offline()
