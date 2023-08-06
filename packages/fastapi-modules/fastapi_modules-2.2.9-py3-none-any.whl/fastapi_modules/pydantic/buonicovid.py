from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TaglioBuono(BaseModel):
    id: int
    cifra: str
    numero: int

    class Config:
        orm_mode = True


class ACQDettagli(BaseModel):
    id: Optional[int] = None
    id_buono: int
    qta: int
    dt_inserimento: Optional[datetime] = None
    id_testata: int

    class Config:
        orm_mode = True


class Acquisizione(BaseModel):
    id: Optional[int] = None
    piva: str
    dt_creazione: Optional[datetime] = None
    dettagli: Optional[List[ACQDettagli]] = []

    class Config:
        orm_mode = True


class Impresa(BaseModel):
    piva: str
    partita_iva: str
    rag_soc: str
    ragione_sociale: str
    acquisizioni: Optional[List[Acquisizione]] = []

    class Config:
        orm_mode = True
