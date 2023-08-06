import datetime
from typing import Optional, List, Union

from pydantic import BaseModel


class OfferteVolentini(BaseModel):
    id: int
    descrizione: str

    class Config:
        orm_mode = True


class LineeVolantini(BaseModel):
    id: int
    descrizione: str

    class Config:
        orm_mode = True


class NegoziVolantini(BaseModel):
    cod_negozio: str
    des_negozio: str

    class Config:
        orm_mode = True


class StatoRichiesta(BaseModel):
    codice: int
    descrizione: str

    class Config:
        orm_mode = True


class RichiesteVol(BaseModel):
    id: Optional[int] = None
    anno: str
    offerta: Union[int, OfferteVolentini]
    linea: Union[int, LineeVolantini]
    punto_vendita: Union[str, NegoziVolantini]
    dt_inizio: datetime.date
    dt_fine: datetime.date
    invio_ora: bool
    dt_creazione: Optional[datetime.datetime] = None
    emails: List[str] = []
    utente: Optional[str] = None
    stato: Union[StatoRichiesta, int] = None

    class Config:
        orm_mode = True
