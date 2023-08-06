from sqlalchemy import String, Column
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DimNegozio(Base):
    __tablename__ = "dim_negozio"
    __table_args__ = {"schema": __file__.split('/')[len(__file__.split('/'))-1].split(".")[0].split("_")[1]}

    cod_negozio = Column(String(3), nullable=False, primary_key=True)
    des_negozio = Column(String(30), nullable=False, unique=True)
