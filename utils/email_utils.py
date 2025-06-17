import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from datetime import datetime

# Carregar variáveis de ambiente do .env
load_dotenv()

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))


def enviar_email_notificacao(nome_escola, email_responsavel):
    try:
        msg = EmailMessage()
        msg['Subject'] = f'📥 Novo Formulário Preenchido - {nome_escola}'
        msg['From'] = EMAIL_USER
        msg['To'] = "administrativo.education@cidadeviva.org"

        corpo = f"""
        Olá equipe,

        Um novo formulário foi preenchido no sistema Cidade Viva Education.

        Nome da Escola: {nome_escola}
        Email do Responsável: {email_responsavel}
        Data de Envio: {datetime.now().strftime('%d/%m/%Y %H:%M')}

        Por favor, acesse o sistema para conferir os detalhes do formulário preenchido.

        ------------------------------
        Este é um email automático enviado pelo Cidade Viva Education.
        """

        msg.set_content(corpo)

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as smtp:
            smtp.starttls()
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)

        print("✅ Email de notificação enviado com sucesso!")

    except Exception as e:
        print(f"❌ Erro ao enviar email de notificação: {e}")
