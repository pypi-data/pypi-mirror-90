from datetime import datetime

from sqlalchemy import String, Column, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from .pgsql_ods import DimNegozio

Base = declarative_base()


class Offerte(Base):
    __tablename__ = "offerte"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    id = Column(Integer, nullable=False, primary_key=True)
    descrizione = Column(String(50), nullable=False, unique=True)


class Linee(Base):
    __tablename__ = "linee"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    id = Column(Integer, nullable=False, primary_key=True)
    descrizione = Column(String(50), nullable=False, unique=True)


class OfferteAnni(Base):
    __tablename__ = "offerte_anni"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    id_offerta = Column(Integer, nullable=False, primary_key=True)
    anno = Column(String(4), nullable=False, primary_key=True)


class OfferteLinee(Base):
    __tablename__ = "offerte_linee"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    id_offerta = Column(Integer, nullable=False, primary_key=True)
    id_linea = Column(Integer, nullable=False, primary_key=True)


class LineeNegozi(Base):
    __tablename__ = "linee_negozi"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    id_linea = Column(Integer, nullable=False, primary_key=True)
    cod_negozio = Column(String(3), nullable=False, primary_key=True)


class Richieste(Base):
    __tablename__ = "richieste"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    id = Column(Integer, nullable=False, primary_key=True)
    anno = Column(String(4), nullable=False)
    id_offerta = Column(Integer, ForeignKey(Offerte.id), nullable=False)
    id_linea = Column(Integer, ForeignKey(Linee.id), nullable=False)
    cod_negozio = Column(String(3), ForeignKey(DimNegozio.cod_negozio), nullable=False)
    dt_inizio = Column(DateTime, nullable=False)
    dt_fine = Column(DateTime, nullable=False)
    invio_ora = Column(Boolean, nullable=False)
    dt_creazione = Column(DateTime, nullable=False, default=datetime.now())
    utente = Column(String(30), nullable=False)
    stato = Column(Integer, nullable=False, default=1)

    emails = relationship("RichiesteEmail", back_populates="richiesta")
    punto_vendita = relationship(DimNegozio)
    offerta = relationship(Offerte)
    linea = relationship(Linee)


class RichiesteEmail(Base):
    __tablename__ = "richieste_email"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    id_richiesta = Column(Integer, ForeignKey(Richieste.id), nullable=False, primary_key=True)
    email = Column(String(80), nullable=False, primary_key=True)

    richiesta = relationship(Richieste, back_populates="emails")
