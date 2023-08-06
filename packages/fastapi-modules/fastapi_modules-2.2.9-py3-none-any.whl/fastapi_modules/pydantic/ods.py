from pydantic import BaseModel


class DimNegozio(BaseModel):
    cod_negozio: str
    des_negozio: str

    class Config:
        orm_mode = True
