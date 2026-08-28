import os
import sys
import pandas as pd
from datetime import timedelta
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

# Aggiungi il path principale per i moduli interni
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from backend.models import Lettura, Sensore
from backend.database import SessionLocal

def evaluate_metrics():
    print("Inizio calcolo metriche...")
    db = SessionLocal()
    
    # Prendi tutte le letture dei sensori dell'acqua ordinate per timestamp
    letture_acqua = db.query(Lettura).join(Sensore).filter(Sensore.tipo == "Acqua").order_by(Lettura.timestamp).all()
    
    total = len(letture_acqua)
    print(f"Totale letture acquisite: {total}")
    
    if total == 0:
        print("Nessuna lettura trovata.")
        return
        
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    
    # Per una migliore simulazione dell'analisi (escludere il warm-up)
    # Ignoriamo i primi 14 giorni di training puro
    min_timestamp = letture_acqua[0].timestamp
    test_start_time = min_timestamp + timedelta(days=14)
    
    analyzed_letture = [l for l in letture_acqua if l.timestamp > test_start_time]
    print(f"Esclusi i primi 14 giorni come training phase (fino al {test_start_time.strftime('%Y-%m-%d %H:%M')}).")
    
    total_analyzed = len(analyzed_letture)
    print(f"Totale letture analizzate nel periodo di test: {total_analyzed}")
    
    for l in analyzed_letture:
        if l.is_ground_truth_anomaly:
            if l.is_anomalia:
                TP += 1
            else:
                FN += 1
        else:
            if l.is_anomalia:
                FP += 1
            else:
                TN += 1
                
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    print("-" * 30)
    print("RISULTATI SPERIMENTALI")
    print("-" * 30)
    print(f"True Positives (TP): {TP}")
    print(f"True Negatives (TN): {TN}")
    print(f"False Positives (FP): {FP}")
    print(f"False Negatives (FN): {FN}")
    print("-" * 30)
    print(f"Precision: {precision:.4f} ({precision*100:.2f}%)")
    print(f"Recall:    {recall:.4f} ({recall*100:.2f}%)")
    print(f"F1-Score:  {f1_score:.4f} ({f1_score*100:.2f}%)")
    
    # Salva in CSV
    import json
    results = {
        "Metric": ["Total Samples Analyzed", "True Positives (TP)", "True Negatives (TN)", "False Positives (FP)", "False Negatives (FN)", "Precision", "Recall", "F1-Score"],
        "Value": [total_analyzed, TP, TN, FP, FN, precision, recall, f1_score]
    }
    df = pd.DataFrame(results)
    df.to_csv("evaluation_results.csv", index=False)
    
    # Salva anche in JSON per conformità
    with open("evaluation_results.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\nRisultati esportati in evaluation_results.csv e evaluation_results.json")
    
    db.close()

if __name__ == "__main__":
    evaluate_metrics()
