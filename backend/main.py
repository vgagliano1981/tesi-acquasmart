from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
import pandas as pd
import io

from . import models, schemas
from .database import SessionLocal, engine
from .mqtt_client import start_mqtt
from datetime import datetime, timedelta

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="IoT Water Monitoring")

# Start MQTT Background Task
@app.on_event("startup")
async def startup_event():
    start_mqtt()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API Scuole
@app.get("/api/scuole", response_model=List[schemas.Scuola])
def read_scuole(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    scuole = db.query(models.Scuola).offset(skip).limit(limit).all()
    return scuole

@app.post("/api/scuole", response_model=schemas.Scuola)
def create_scuola(scuola: schemas.ScuolaCreate, db: Session = Depends(get_db)):
    db_scuola = models.Scuola(**scuola.dict())
    db.add(db_scuola)
    db.commit()
    db.refresh(db_scuola)
    return db_scuola

@app.delete("/api/scuole/{scuola_id}")
def delete_scuola(scuola_id: int, db: Session = Depends(get_db)):
    scuola = db.query(models.Scuola).filter(models.Scuola.id == scuola_id).first()
    if not scuola:
        raise HTTPException(status_code=404, detail="Scuola not found")
    db.delete(scuola)
    db.commit()
    return {"ok": True}

@app.put("/api/scuole/{scuola_id}", response_model=schemas.Scuola)
def update_scuola(scuola_id: int, scuola_update: schemas.ScuolaCreate, db: Session = Depends(get_db)):
    scuola = db.query(models.Scuola).filter(models.Scuola.id == scuola_id).first()
    if not scuola:
        raise HTTPException(status_code=404, detail="Scuola not found")
    
    scuola.nome = scuola_update.nome
    scuola.indirizzo = scuola_update.indirizzo
    scuola.numero_studenti = scuola_update.numero_studenti
    scuola.codice_meccanografico = scuola_update.codice_meccanografico
    
    db.commit()
    db.refresh(scuola)
    return scuola

@app.get("/api/scuole/{scuola_id}/sensori", response_model=List[schemas.Sensore])
def read_scuola_sensori(scuola_id: int, db: Session = Depends(get_db)):
    return db.query(models.Sensore).filter(models.Sensore.scuola_id == scuola_id).all()

@app.get("/api/scuole/{scuola_id}/stato_sensori")
def read_stato_sensori(scuola_id: int, db: Session = Depends(get_db)):
    sensori = db.query(models.Sensore).filter(models.Sensore.scuola_id == scuola_id).all()
    stato = []
    for s in sensori:
        ultima_lettura = db.query(models.Lettura).filter(models.Lettura.sensore_id == s.id)\
                            .order_by(models.Lettura.timestamp.desc()).first()
        valore = ultima_lettura.valore_litri if ultima_lettura else 0.0
        anomalia = ultima_lettura.is_anomalia if ultima_lettura else False
        stato.append({
            "id": s.id,
            "nome": s.nome,
            "tipo": s.tipo,
            "is_main": s.is_main,
            "valore_attuale": valore,
            "is_anomalia": anomalia
        })
    return stato

@app.post("/api/sensori", response_model=schemas.Sensore)
def create_sensore(sensore: schemas.SensoreCreate, db: Session = Depends(get_db)):
    db_sensore = models.Sensore(
        scuola_id=sensore.scuola_id,
        tipo=sensore.tipo,
        topic_mqtt=sensore.topic_mqtt,
        nome=sensore.nome,
        is_main=sensore.is_main
    )
    db.add(db_sensore)
    db.commit()
    db.refresh(db_sensore)
    
    # Riavvia il simulatore se è attivo (opzionale, o basta attendere)
    return db_sensore

# API Letture e Sensori
@app.get("/api/letture", response_model=List[schemas.LetturaConScuola])
def read_letture(limit: int = 1000, scuola_id: int = None, hours_offset: int = 0, db: Session = Depends(get_db)):
    # Finestra temporale: da (Adesso - (hours_offset+1) ore) a (Adesso - hours_offset ore)
    now = datetime.now()
    end_time = now - timedelta(hours=hours_offset)
    start_time = end_time - timedelta(hours=1)

    query = db.query(
        models.Lettura.id,
        models.Lettura.sensore_id,
        models.Lettura.timestamp,
        models.Lettura.valore_litri,
        models.Lettura.is_anomalia,
        models.Lettura.anomaly_score,
        models.Scuola.nome.label("scuola_nome"),
        models.Sensore.nome.label("sensore_nome"),
        models.Sensore.is_main.label("sensore_is_main")
    ).join(models.Sensore, models.Lettura.sensore_id == models.Sensore.id)\
     .join(models.Scuola, models.Sensore.scuola_id == models.Scuola.id)\
     .filter(models.Lettura.timestamp >= start_time, models.Lettura.timestamp <= end_time)

    if scuola_id is not None and scuola_id > 0:
        query = query.filter(models.Scuola.id == scuola_id)
        
    results = query.order_by(models.Lettura.timestamp.desc()).limit(limit).all()
    
    # Convertiamo i risultati in dizionari compatibili con LetturaConScuola
    out = []
    for r in results:
        out.append({
            "id": r.id,
            "sensore_id": r.sensore_id,
            "timestamp": r.timestamp,
            "valore_litri": r.valore_litri,
            "is_anomalia": r.is_anomalia,
            "anomaly_score": r.anomaly_score,
            "scuola_nome": r.scuola_nome,
            "sensore_nome": r.sensore_nome,
            "sensore_is_main": r.sensore_is_main
        })
    return out

@app.get("/api/aggregati_consumi")
def read_aggregati_consumi(scuola_id: int = None, db: Session = Depends(get_db)):
    now = datetime.now()
    start_of_hour = now - timedelta(hours=1)
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    start_of_week = start_of_day - timedelta(days=now.weekday())
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    base_query = db.query(func.sum(models.Lettura.valore_litri)).join(models.Sensore, models.Lettura.sensore_id == models.Sensore.id).filter(models.Sensore.tipo.not_in(["Pressione", "Torbidità", "Conducibilità"]))
    if scuola_id is not None and scuola_id > 0:
        base_query = base_query.filter(models.Sensore.scuola_id == scuola_id)

    consumo_orario = base_query.filter(models.Lettura.timestamp >= start_of_hour).scalar() or 0.0
    consumo_giornaliero = base_query.filter(models.Lettura.timestamp >= start_of_day).scalar() or 0.0
    consumo_settimanale = base_query.filter(models.Lettura.timestamp >= start_of_week).scalar() or 0.0
    consumo_mensile = base_query.filter(models.Lettura.timestamp >= start_of_month).scalar() or 0.0

    return {
        "consumo_orario": consumo_orario,
        "consumo_giornaliero": consumo_giornaliero,
        "consumo_settimanale": consumo_settimanale,
        "consumo_mensile": consumo_mensile
    }

@app.get("/api/confronto_consumi")
def confronto_consumi(scuola_id: int, start_date: datetime, end_date: datetime, db: Session = Depends(get_db)):
    # Somma il consumo d'acqua per i sensori principali della scuola in un intervallo di tempo
    # Restituisce i litri totali
    base_query = db.query(func.sum(models.Lettura.valore_litri))\
                   .join(models.Sensore, models.Lettura.sensore_id == models.Sensore.id)\
                   .filter(models.Sensore.scuola_id == scuola_id)\
                   .filter(models.Sensore.is_main == True)\
                   .filter(models.Sensore.tipo == "Acqua")\
                   .filter(models.Lettura.timestamp >= start_date)\
                   .filter(models.Lettura.timestamp <= end_date)
                   
    totale_litri = base_query.scalar() or 0.0
    
    return {
        "scuola_id": scuola_id,
        "start_date": start_date,
        "end_date": end_date,
        "consumo_simulato_litri": totale_litri
    }

@app.get("/api/ricerca_misurazione", response_model=List[schemas.LetturaConScuola])
def ricerca_misurazione(target_time: datetime, scuola_id: int = None, db: Session = Depends(get_db)):
    # Limit search space to +/- 12 hours from target_time to avoid full table scans if table is huge
    start_time = target_time - timedelta(hours=12)
    end_time = target_time + timedelta(hours=12)

    query = db.query(
        models.Lettura.id,
        models.Lettura.sensore_id,
        models.Lettura.timestamp,
        models.Lettura.valore_litri,
        models.Lettura.is_anomalia,
        models.Lettura.anomaly_score,
        models.Scuola.nome.label("scuola_nome"),
        models.Sensore.nome.label("sensore_nome"),
        models.Sensore.is_main.label("sensore_is_main")
    ).join(models.Sensore, models.Lettura.sensore_id == models.Sensore.id)\
     .join(models.Scuola, models.Sensore.scuola_id == models.Scuola.id)\
     .filter(models.Lettura.timestamp >= start_time, models.Lettura.timestamp <= end_time)

    if scuola_id is not None and scuola_id > 0:
        query = query.filter(models.Scuola.id == scuola_id)
    else:
        # Se cerchiamo in tutte le scuole, mostriamo solo i contatori principali per non affollare la UI
        query = query.filter(models.Sensore.is_main == True)

    results = query.all()
    
    # Trova il record con la minima distanza temporale per ogni sensore
    closest_per_sensor = {}
    for r in results:
        diff = abs((r.timestamp - target_time).total_seconds())
        sensore_id = r.sensore_id
        if sensore_id not in closest_per_sensor:
            closest_per_sensor[sensore_id] = (diff, r)
        else:
            if diff < closest_per_sensor[sensore_id][0]:
                closest_per_sensor[sensore_id] = (diff, r)
    
    out = []
    for diff, r in closest_per_sensor.values():
        out.append({
            "id": r.id,
            "sensore_id": r.sensore_id,
            "timestamp": r.timestamp,
            "valore_litri": r.valore_litri,
            "is_anomalia": r.is_anomalia,
            "anomaly_score": r.anomaly_score,
            "scuola_nome": r.scuola_nome,
            "sensore_nome": r.sensore_nome,
            "sensore_is_main": r.sensore_is_main
        })
    
    # Ordiniamo per nome scuola
    out.sort(key=lambda x: (x["scuola_nome"], x["sensore_nome"]))
    return out

@app.get("/api/allarmi", response_model=List[schemas.AllarmeOut])
def read_allarmi(limit: int = 50, db: Session = Depends(get_db)):
    query = db.query(
        models.Lettura.id,
        models.Lettura.timestamp,
        models.Lettura.valore_litri,
        models.Lettura.anomaly_score,
        models.Scuola.nome.label("scuola_nome"),
        models.Sensore.nome.label("sensore_nome"),
        models.Sensore.is_main.label("is_main")
    ).join(models.Sensore, models.Lettura.sensore_id == models.Sensore.id)\
     .join(models.Scuola, models.Sensore.scuola_id == models.Scuola.id)\
     .filter(models.Lettura.is_anomalia == True)
    
    results = query.order_by(models.Lettura.timestamp.desc()).limit(limit).all()
    
    out = []
    for r in results:
        out.append({
            "id": r.id,
            "timestamp": r.timestamp,
            "valore_litri": r.valore_litri,
            "anomaly_score": r.anomaly_score,
            "scuola_nome": r.scuola_nome,
            "sensore_nome": r.sensore_nome,
            "is_main": r.is_main,
            "email_inviata": True
        })
    return out



# API per dati reali manuali
@app.post("/api/dati_reali", response_model=schemas.DatoReale)
def create_dato_reale(dato: schemas.DatoRealeCreate, db: Session = Depends(get_db)):
    db_dato = models.DatoReale(**dato.dict())
    db.add(db_dato)
    db.commit()
    db.refresh(db_dato)
    return db_dato

@app.get("/api/dati_reali", response_model=List[schemas.DatoReale])
def read_dati_reali(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.DatoReale).offset(skip).limit(limit).all()

# API per upload CSV Dati Reali
@app.post("/api/upload_csv")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV.")
    
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
        
        # Ci aspettiamo colonne: nome_scuola, indirizzo_scuola, codice_contratto_acqua, codice_meccanografico, data_inizio, data_fine, consumo
        required_cols = ['nome_scuola', 'indirizzo_scuola', 'codice_contratto_acqua', 'codice_meccanografico', 'data_inizio', 'data_fine', 'consumo']
        
        if not all(col in df.columns for col in required_cols):
            return {"message": "Formato CSV non valido. Colonne mancanti.", "righe": 0}
            
        added = 0
        for _, row in df.iterrows():
            try:
                dato = models.DatoReale(
                    nome_scuola=str(row['nome_scuola']),
                    indirizzo_scuola=str(row['indirizzo_scuola']),
                    codice_contratto_acqua=str(row['codice_contratto_acqua']),
                    codice_meccanografico=str(row['codice_meccanografico']),
                    data_inizio=pd.to_datetime(row['data_inizio']).to_pydatetime(),
                    data_fine=pd.to_datetime(row['data_fine']).to_pydatetime(),
                    consumo=float(row['consumo'])
                )
                db.add(dato)
                added += 1
            except Exception as e:
                print(f"Errore parsing riga: {e}")
                
        db.commit()
        return {"message": "CSV caricato con successo", "righe": added, "data": []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore durante l'elaborazione del CSV: {str(e)}")

import re
import PyPDF2

@app.post("/api/upload_pdf_bolletta")
async def upload_pdf_bolletta(file: UploadFile = File(...)):
    if not file.filename.lower().endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Il file deve essere un PDF.")
    
    contents = await file.read()
    testo = ""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(contents))
        for page in reader.pages:
            testo += page.extract_text() + " "
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore lettura PDF: {str(e)}")
        
    date_pattern = r'\b(\d{2}[/-]\d{2}[/-]\d{4})\b'
    consumo_pattern = r'\b(\d+[,.]\d+|\d+)\s*(?:mc|m3|metri\s*cubi)\b'
    
    date_trovate = re.findall(date_pattern, testo)
    consumi_trovati = re.findall(consumo_pattern, testo, re.IGNORECASE)
    
    data_inizio = date_trovate[0] if len(date_trovate) > 0 else ""
    data_fine = date_trovate[1] if len(date_trovate) > 1 else ""
    consumo = consumi_trovati[0] if consumi_trovati else ""
    if consumo:
        consumo = consumo.replace(',', '.')
        
    return {
        "success": True,
        "data_inizio": data_inizio.replace('-', '/'),
        "data_fine": data_fine.replace('-', '/'),
        "consumo_mc": consumo
    }

@app.get("/api/storico_confronti")
def storico_confronti(scuola_id: int = None, db: Session = Depends(get_db)):
    query = db.query(models.DatoReale)
    if scuola_id and scuola_id > 0:
        scuola = db.query(models.Scuola).filter(models.Scuola.id == scuola_id).first()
        if scuola:
            query = query.filter(models.DatoReale.nome_scuola == scuola.nome)
            
    dati = query.order_by(models.DatoReale.data_inizio.asc()).all()
    
    risultati = []
    for d in dati:
        scuola_obj = db.query(models.Scuola).filter(models.Scuola.nome == d.nome_scuola).first()
        consumo_simulato = 0.0
        if scuola_obj:
            sensore_main = db.query(models.Sensore).filter(
                models.Sensore.scuola_id == scuola_obj.id,
                models.Sensore.is_main == True
            ).first()
            if sensore_main:
                consumo_simulato = db.query(func.sum(models.Lettura.valore_litri)).filter(
                    models.Lettura.sensore_id == sensore_main.id,
                    models.Lettura.timestamp >= d.data_inizio,
                    models.Lettura.timestamp <= d.data_fine
                ).scalar() or 0.0

        risultati.append({
            "id": d.id,
            "periodo": f"{d.data_inizio.strftime('%m/%y')} - {d.data_fine.strftime('%m/%y')}",
            "nome_scuola": d.nome_scuola,
            "consumo_bolletta_litri": d.consumo * 1000, 
            "consumo_simulato_litri": consumo_simulato
        })
    return risultati

# Mount static files (Frontend HTML/CSS/JS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
def read_root():
    return FileResponse("frontend/index.html", headers={"Cache-Control": "no-cache, no-store, must-revalidate"})
