import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.models import Base, Scuola, Sensore, Lettura, DatoReale
import datetime

# 1. Recupera l'URL di PostgreSQL
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    print("ERRORE: Inserisci il link di Neon.tech. Usa il comando 'set DATABASE_URL=postgresql://...' prima di avviare questo script.")
    exit(1)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# 2. Crea tabelle su PostgreSQL
print("Connessione a PostgreSQL in corso...")
pg_engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=pg_engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pg_engine)
pg_db = SessionLocal()

# 3. Connettiti a SQLite locale
print("Connessione al database locale SQLite...")
sqlite_conn = sqlite3.connect('iot_platform.db')
cursor = sqlite_conn.cursor()

def parse_dt(dt_str):
    if not dt_str: return None
    try:
        if '.' in dt_str:
            return datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S.%f')
        return datetime.datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
    except:
        return None

# COPIA SCUOLE
print("Copia delle scuole...")
cursor.execute("SELECT id, nome, indirizzo, numero_studenti, codice_meccanografico FROM scuole")
scuole = cursor.fetchall()
for s in scuole:
    # Evita duplicati se lo script viene lanciato due volte
    if not pg_db.query(Scuola).filter(Scuola.id == s[0]).first():
        pg_db.add(Scuola(id=s[0], nome=s[1], indirizzo=s[2], numero_studenti=s[3], codice_meccanografico=s[4]))
pg_db.commit()

# COPIA SENSORI
print("Copia dei sensori...")
cursor.execute("SELECT id, scuola_id, nome, is_main, tipo, topic_mqtt FROM sensori")
sensori = cursor.fetchall()
for s in sensori:
    if not pg_db.query(Sensore).filter(Sensore.id == s[0]).first():
        pg_db.add(Sensore(id=s[0], scuola_id=s[1], nome=s[2], is_main=bool(s[3]), tipo=s[4], topic_mqtt=s[5]))
pg_db.commit()

# COPIA DATI REALI (BOLLETTE)
print("Copia dello storico bollette...")
cursor.execute("SELECT id, nome_scuola, indirizzo_scuola, codice_contratto_acqua, codice_meccanografico, data_inizio, data_fine, consumo FROM dati_reali")
dati_reali = cursor.fetchall()
for d in dati_reali:
    if not pg_db.query(DatoReale).filter(DatoReale.id == d[0]).first():
        pg_db.add(DatoReale(
            id=d[0], nome_scuola=d[1], indirizzo_scuola=d[2], codice_contratto_acqua=d[3], 
            codice_meccanografico=d[4], data_inizio=parse_dt(d[5]), data_fine=parse_dt(d[6]), consumo=d[7]
        ))
pg_db.commit()

print("Tutti i dati principali (scuole, sensori, storico bollette) sono stati copiati su Neon!")
print("Se ricarichi il sito live, vedrai di nuovo tutte le tue scuole e i tuoi sensori al loro posto.")
