import json
from fastapi import FastAPI
from pydantic import BaseModel
from api.infra.config.database import buscar, atualizaSitEmail, inserindoEmail, buscarsituacao
from api.infra.repositorios.repositoriosFuncs import validaCampo, validaCampoEmail, validaEmail, enviaremail


class Item(BaseModel):
    chave: int
    email: str
    assunto: str
    corpo: str


app = FastAPI(debug=True)


@app.post("/items/")
async def create_item(item: Item):
    #validaremailok(item.email)
    if buscar(item.chave, "instituicao", "chave_toker") == False:
        return json.dumps({'status': 'Nao Enviado! verifique sua chave!', 'chave inserida': item.chave})
    else:
        item.email = item.email.replace(" ","").lower() #tirar os espaço em branco e as letras maiusculas em minusculas
        if validaCampo(item.email) == False:
            return json.dumps({'status': 'Nao Enviado! verifique se o campo endereco de email esta vazio!', 'endereco': item.email})
       
        #validando email
        vEmail, item.email, dominio = validaEmail(item.email) #função retornando boleano e str
        if buscar(dominio,"dominio_email","dominio") == False:
            inserindoEmail(item.email, "lista_email2", item.chave)
            return json.dumps({'status': 'Nao Enviado! verifique o dominio do email!', 'endereco': item.email})
            
        #busca no banco e insere no caso de não existir no banco
        if buscar(item.email, "lista_email2", "email") != True:
            inserindoEmail(item.email, "lista_email2", item.chave)

        #definir a situação do email no banco
        if vEmail == True: 
            if buscarsituacao(item.email, "lista_email2", "email", 2) == False:
                atualizaSitEmail("lista_email2", 2, item.email) #para validos 
        else:
            if buscarsituacao(item.email, "lista_email2", "email", 1) == False:
                atualizaSitEmail("lista_email2", 1, item.email) #para invalidos

         #enviar email
        if validaCampo(item.assunto) == True and validaCampo(item.corpo) == True:
            if buscarsituacao(item.email, "lista_email2", "email", 2) == True:
                #enviaremail(item.assunto, item.corpo, item.email)
                return json.dumps({'chave': item.chave, 'assunto do email': item.assunto, 'corpo do email': item.corpo, 'destinatario': item.email, 'status': 'Enviado!'})
            else:
                return json.dumps({'status': 'Nao Enviado! verifique o endereco de email...', 'destinatario': item.email})
        elif validaCampo(item.assunto) == False:
            return json.dumps({'status': 'Nao Enviado! verifique se o campo Assunto esta vazio!', 'assunto do email': item.assunto})
        elif validaCampo(item.corpo) == False:
            return json.dumps({'status': 'Nao Enviado! verifique se o campo Corpo do email esta vazio!', 'corpo do email': item.corpo})
        else:
            return json.dumps({'status': 'Nao Enviado! verifique se o campo Assunto e Corpo do email estao vazio!', 'assunto do email': item.assunto , 'corpo do email': item.corpo})
