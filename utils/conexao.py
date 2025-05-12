import psycopg2
from dotenv import load_dotenv
import os

# Carregar variáveis do .env
load_dotenv()

def conectar():
    try:
        conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
        )
        print("Conexão bem-sucedida!")
        return conn
    except Exception as e:
        print(f"Erro: {e}")
        return None

def verificar_status_banco():
    try:
        conn = conectar()
        conn.close()
        return '<span style="color:green;">🟢 Banco Conectado</span>'
    except Exception as e:
        return f"<span style='color:red;'>🔴 Falha na Conexão: {str(e)}</span>"
 