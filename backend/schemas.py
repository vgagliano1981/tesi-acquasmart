from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScuolaBase(BaseModel):
    nome: str
    indirizzo: str
    numero_studenti: int
    codice_meccanografico: Optional[str] = None

class ScuolaCreate(ScuolaBase):
    pass

class Scuola(ScuolaBase):
    id: int

    class Config:
        from_attributes = True

class SensoreBase(BaseModel):
    tipo: str
    topic_mqtt: str
    nome: str = "Sensore"
    is_main: bool = False

class SensoreCreate(SensoreBase):
    scuola_id: int

class Sensore(SensoreBase):
    id: int
    scuola_id: int

    class Config:
        from_attributes = True

class LetturaBase(BaseModel):
    valore_litri: float
    is_anomalia: bool
    anomaly_score: float

class LetturaCreate(LetturaBase):
    sensore_id: int
    timestamp: datetime

class Lettura(LetturaBase):
    id: int
    sensore_id: int
    timestamp: datetime
    is_anomalia: bool
    anomaly_score: float

    class Config:
        from_attributes = True

class LetturaConScuola(Lettura):
    scuola_nome: str
    sensore_nome: str
    sensore_is_main: bool

class AllarmeOut(BaseModel):
    id: int
    timestamp: datetime
    valore_litri: float
    anomaly_score: float
    scuola_nome: str
    sensore_nome: str
    is_main: bool
    email_inviata: bool = True

    class Config:
        from_attributes = True

class DatoRealeBase(BaseModel):
    nome_scuola: str
    indirizzo_scuola: str
    codice_contratto_acqua: str
    codice_meccanografico: str
    data_inizio: datetime
    data_fine: datetime
    consumo: float

class DatoRealeCreate(DatoRealeBase):
    pass

class DatoReale(DatoRealeBase):
    id: int

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        from_attributes = True
