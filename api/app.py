from flask import Flask, render_template, request, redirect, url_for, Response
import json
from infra.config.database import buscar, atualizaSitEmail, conectar, close, inserindoEmail, buscarsituacao
from infra.repositorios.repositoriosFuncs import validaCampo, validaCampoEmail, validaEmail, enviaremail


app = Flask(__name__, template_folder="public")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/erro')
def erro():
    return render_template('erro.html')

@app.route('/validar', methods=['GET','POST'])
def validaChave():
    if request.method == 'POST':
        chave = request.form['chave']
        email = request.form['endereco']
        assunto = request.form['assunto'] 
        corpo = request.form['corpo']

        validar = buscar(chave, "instituicao", "chave_toker")
        if validar == True:
            frase = " "
            if validaCampo(email) == False:
                return json.dumps({'status': 'Nao Enviado! verifique se o campo endereco de email esta vazio!', 'endereco': email})
            elif frase not in email:
                a = buscar(email, "lista_email2", "email")
            else:
                teste = email.replace(" ","")
                a = buscar(teste, "lista_email2", "email")
                email = teste
            #inserindo e validando email
            if a != True:
                inserindoEmail(email, "lista_email2", chave)
            teste = validaEmail(email)
            if teste == True: 
                if buscarsituacao(email, "lista_email2", "email", 2) == False:
                    atualizaSitEmail("lista_email2", 2, email) #para validos 
            else:
                if buscarsituacao(email, "lista_email2", "email", 1) == False:
                    atualizaSitEmail("lista_email2", 1, email) #para invalidos
            
            #enviar email
            if validaCampo(assunto) == True and validaCampo(corpo) == True:
                if buscarsituacao(email, "lista_email2", "email", 2) == True:
                    enviaremail(assunto, corpo, email)
                    return json.dumps({'chave': chave, 'assunto do email': assunto, 'corpo do email': corpo, 'destinatario': email, 'status': 'Enviado!'})
                    #print("Email enviado!")
                else:
                    return json.dumps({'status': 'Nao Enviado! verifique o endereco de email...', 'destinatario': email})
            elif validaCampo(assunto) == False:
                return json.dumps({'status': 'Nao Enviado! verifique se o campo Assunto esta vazio!', 'assunto do email': assunto})
            elif validaCampo(corpo) == False:
                return json.dumps({'status': 'Nao Enviado! verifique se o campo Corpo do email esta vazio!', 'corpo do email': corpo})
            else:
                return json.dumps({'status': 'Nao Enviado! verifique se o campo Assunto e Corpo do email estao vazio!', 'assunto do email': assunto , 'corpo do email': corpo})
        return json.dumps({'status': 'Nao Enviado! verifique sua chave!', 'chave inserida': chave}) #redirect(url_for('erro'))


if __name__ == "__main__":
    app.run(debug=True, host='10.0.0.118', port='3000')