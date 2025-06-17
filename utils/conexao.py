import psycopg2
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine


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


# ==== Dados do Email ====
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")


# 🔗 Conexão com SQLAlchemy (para integração com pandas)
def conectar_sqlalchemy():
    try:
        url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(url)
        print("✅ Conexão SQLAlchemy bem-sucedida.")
        return engine
    except Exception as e:
        print(f"❌ Erro na conexão SQLAlchemy: {e}")
        return None
