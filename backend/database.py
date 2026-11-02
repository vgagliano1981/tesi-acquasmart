import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cerchiamo la variabile d'ambiente DATABASE_URL
DATABASE_URL = os.environ.get("DATABASE_URL")
engine = None

if DATABASE_URL:
    # Fix per Render: assicuriamoci di usare il driver psycopg2
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
        
    try:
        temp_engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"connect_timeout": 5})
        with temp_engine.connect() as conn:
            pass
        engine = temp_engine
        print("Connessione a PostgreSQL stabilita con successo!")
    except Exception as e:
        print(f"PostgreSQL non disponibile ({e}). Fallback automatico su SQLite locale (iot_platform.db).")
        engine = None

if engine is None:
    # Se non c'è DATABASE_URL o la connessione fallisce (es. database cloud scaduto), usiamo SQLite locale
    SQLALCHEMY_DATABASE_URL = "sqlite:///./iot_platform.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    print("Utilizzo database SQLite locale: iot_platform.db")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
