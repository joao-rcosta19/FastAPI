import validate_email
from email_validator import validate_email, EmailNotValidError
import smtplib #Protocolo de transferência de email simples
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def validaCampo(campo):
    if not campo or campo.isspace() == True:
        return False
    else:
        return True

def validaCampoEmail(campo, obs):
    while True:
        n = False
        if not campo or campo.isspace() == True:
            print(f"ERRO! {obs} Vazio!")
            campo = input(f"Digite o {obs}: ").replace(" ","")
            #return False
        else:
            #print(f"{obs} ok!")
            return True
            break

def validaEmail(email):
    is_new_account = True
    try:
        validation = validate_email(email, check_deliverability = is_new_account)
        email = validation.email
    except EmailNotValidError as e:
        print(str(e))
        return False #caso seja invalido
    print(" e-mail validado: ", email)
    return True #caso seja valido


def enviaremail(assunto, texto, endereco):
    # Inciar o Servidor SMTP
    host = "smtp.gmail.com"
    port = "587"
    login = "conexaodigitalcameta@gmail.com"
    senha = "hqmfzsasfvbhqxug"

    server = smtplib.SMTP(host, port)

    server.ehlo()
    server.starttls()

    server.login(login, senha)

    #Construindo o email tipo MIME
    corpo_email = f"""
    <p>{texto}</p>
    """

    email_msg = MIMEMultipart()
    email_msg['From'] = login #conta de saida
    email_msg['To'] = endereco #login #"barrasymonn@gmail.com" #emai-l destinatario
    email_msg['Subject'] = assunto #Assunto do E-mail
    email_msg.attach(MIMEText(corpo_email, 'html'))

    #Enviar o email tipo MIME no Servidor SMTP
    server.sendmail(email_msg['From'],email_msg['To'],email_msg.as_string())
    server.quit()
    return True