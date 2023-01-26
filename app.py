from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel
from api.infra.config.database import buscar, atualizaSitEmail, conectar, close, inserindoEmail, buscarsituacao
from api.infra.repositorios.repositoriosFuncs import validaCampo, validaCampoEmail, validaEmail, enviaremail


class Item(BaseModel):
    chave: int
    email: str
    assunto: str
    corpo: str


app = FastAPI()


@app.post("/items/")
async def create_item(item: Item):
    validar = buscar(item.chave, "instituicao", "chave_toker")
    return validar