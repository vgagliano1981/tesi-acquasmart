import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Cerchiamo la variabile d'ambiente DATABASE_URL
DATABASE_URL = os.environ.get("DATABASE_URL")

if DATABASE_URL:
    # Fix per Render: assicuriamoci di usare il driver psycopg2
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+psycopg2://", 1)
    elif DATABASE_URL.startswith("postgresql://"):
        DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+psycopg2://", 1)
        
    engine = create_engine(DATABASE_URL)
else:
    # Se non c'è DATABASE_URL, usiamo il vecchio SQLite locale per lo sviluppo
    SQLALCHEMY_DATABASE_URL = "sqlite:///./iot_platform.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
