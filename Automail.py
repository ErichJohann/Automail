import smtplib
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from email.message import EmailMessage

# Carregar credenciais
SCOPES = ["https://mail.google.com/"] #, "https://www.googleapis.com/auth/userinfo.email"
SERVICE_ACCOUNT_FILE = "client_secret.json"

flow = InstalledAppFlow.from_client_secrets_file(SERVICE_ACCOUNT_FILE, SCOPES)
credentials = flow.run_local_server(port=0) #, include_granted_scopes=False

#print("Escopos obtidos:", credentials.scopes)
#print("Token ID:", credentials.id_token)

SERVER = "smtp.gmail.com"
PORT = 587

try:
    smtp = smtplib.SMTP(SERVER, PORT)
    status, response = smtp.ehlo()
    print(f"[{status}] - {response}")
    smtp.starttls()
    status, response = smtp.ehlo()
    print(f"[{status}] - {response}")

except Exception as e:
    print(f"Erro ao estabelecer conexão smtp: {e}")
    exit(1)


#user = credentials.id_token["email"]
#print(f"Email autenticado: {user}")
user = input("Digite o endereço de email autorizado: ")
dest = input("Entre com o email destinatário: ")

auth = f"user={user}\x01auth=Bearer {credentials.token}\x01\x01"
auth = base64.b64encode(auth.encode()).decode()

try:
    status, response = smtp.docmd("AUTH", "XOAUTH2 " + auth)
    if status != 235:
        print(f"Erro de autenticação: {response.decode()}")
        exit(2)
    print("Conexão bem sucedida!")

    msg = EmailMessage()
    msg["From"] = user
    msg["To"] = dest
    msg["Subject"] = "Envio com OAuth2"
    msg.set_content("Este e-mail foi enviado usando OAuth2 com Python!")

    smtp.send_message(msg)
    print("E-mail enviado com sucesso!")

except Exception as e:
    print(f"Erro ao envar email: {e}")

smtp.quit()