from sqlalchemy import String, Column, Integer, DateTime, func, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class AziendeEsterne(Base):
    __tablename__ = "aziende_esterne"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    piva = Column(String(11), nullable=False, primary_key=True)
    rag_soc = Column(String(100), nullable=False)


class BuoniTagli(Base):
    __tablename__ = "buoni_tagli"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    id = Column(Integer, nullable=False, primary_key=True)
    cifra = Column(String(100), nullable=False, unique=True)
    numero = Column(Integer, nullable=False, unique=True)


class AcquisizioneBuoniTestata(Base):
    __tablename__ = "acquisizione_buoni_testata"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    id = Column(Integer, nullable=False, primary_key=True)
    piva = Column(String(11), ForeignKey(AziendeEsterne.piva), nullable=False)
    dt_creazione = Column(DateTime, nullable=False, default=func.now())

    dettagli = relationship("AcquisizioneBuoniDettagli", uselist=True)
    azienda = relationship(AziendeEsterne, uselist=True)


class AcquisizioneBuoniDettagli(Base):
    __tablename__ = "acquisizione_buoni_dettagli"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    id = Column(Integer, nullable=False, primary_key=True)
    id_taglio_buono = Column(Integer, ForeignKey(BuoniTagli.id), nullable=False)
    qta_buono = Column(Integer, nullable=False)
    dt_inserimento = Column(DateTime, nullable=False, default=func.now())
    id_testata_acquisizione = Column(Integer, ForeignKey(AcquisizioneBuoniTestata.id), nullable=False)

    buono = relationship("BuoniTagli")
