import os
import sys
import base64
import smtplib
import pickle
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import csv

SCOPES = ["https://www.googleapis.com/auth/gmail.send", "https://www.googleapis.com/auth/gmail.readonly", "https://mail.google.com/"]
TOKEN_FILE = "token.pickle"
CLIENT_SECRET_FILE = "client_secret.json"

SERVER = "smtp.gmail.com"
PORT = 587

def get_credentials():
    credentials = None
    
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            credentials = flow.run_local_server(port=0)

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(credentials, token)

    return credentials


def setSMTP():
    try:
        smtp = smtplib.SMTP(SERVER, PORT)
        smtp.starttls()
        return smtp

    except Exception as e:
        print(f"Erro ao estabelecer conexão smtp: {e}")
        exit(1)


def setDest(dest):
    addrs = []
    with open(dest, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')

        next(reader, None)
        for line in reader:
            addrs.append(line[0])

    return addrs


def setContent(msg):
    with open(msg, 'r') as content:
        lines = content.readlines()

    sub = lines[0].strip()
    body = ''.join(lines[1:]).strip()

    return sub, body



def main(dest, msg):
    smtp = setSMTP()
    credentials = get_credentials()

    service = build("gmail", "v1", credentials=credentials)
    user = service.users().getProfile(userId="me").execute()["emailAddress"]
    print(f"Usuário autenticado: {user}")

    auth = f"user={user}\x01auth=Bearer {credentials.token}\x01\x01"
    auth = base64.b64encode(auth.encode()).decode()

    addrs = setDest(dest)
    sub, body = setContent(msg)
    print("Dados da mensagem carregados")

    try:
        status, response = smtp.docmd("AUTH", "XOAUTH2 " + auth)
        if status != 235:
            print(f"Erro de autenticação: [{status}] - {response.decode()}")
            exit(2)
        print("Conexão bem sucedida!")

        msg = EmailMessage()
        msg["From"] = user
        msg["To"] = ', '.join(addrs)
        msg["Subject"] = sub
        msg.set_content(body)

        smtp.send_message(msg)
        print("E-mail enviado com sucesso!")

    except Exception as e:
        print(f"Erro ao envar email: {e}")
    
    smtp.quit()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Uso: python {sys.argv[0]} [destinatarios.csv] [mensagem.txt]")
    else:
        main(sys.argv[1], sys.argv[2])

