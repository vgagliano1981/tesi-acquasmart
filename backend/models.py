from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
import datetime
from .database import Base

class Scuola(Base):
    __tablename__ = "scuole"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    indirizzo = Column(String)
    numero_studenti = Column(Integer)
    codice_meccanografico = Column(String, default="")
    
    sensori = relationship("Sensore", back_populates="scuola")

class Sensore(Base):
    __tablename__ = "sensori"

    id = Column(Integer, primary_key=True, index=True)
    scuola_id = Column(Integer, ForeignKey("scuole.id"))
    nome = Column(String, default="Contatore Principale")
    is_main = Column(Boolean, default=True)
    tipo = Column(String, default="Acqua")
    topic_mqtt = Column(String, unique=True, index=True)
    
    scuola = relationship("Scuola", back_populates="sensori")
    letture = relationship("Lettura", back_populates="sensore")

class Lettura(Base):
    __tablename__ = "letture"

    id = Column(Integer, primary_key=True, index=True)
    sensore_id = Column(Integer, ForeignKey("sensori.id"))
    timestamp = Column(DateTime, default=datetime.datetime.now)
    valore_litri = Column(Float)
    is_anomalia = Column(Boolean, default=False)
    anomaly_score = Column(Float, default=0.0)
    
    sensore = relationship("Sensore", back_populates="letture")

class DatoReale(Base):
    __tablename__ = "dati_reali"

    id = Column(Integer, primary_key=True, index=True)
    nome_scuola = Column(String)
    indirizzo_scuola = Column(String)
    codice_contratto_acqua = Column(String)
    codice_meccanografico = Column(String)
    data_inizio = Column(DateTime)
    data_fine = Column(DateTime)
    consumo = Column(Float, default=0.0) # Consumo in Litri o m3 nel periodo
