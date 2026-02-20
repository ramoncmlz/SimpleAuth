import sqlite3

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

from pathlib import Path

DB_PATH = Path(__file__).with_name("simpleauth.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # faz o select retornar linhas com acesso ao nome da coluna
    return conn

def init_db():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            session_version INTEGER NOT NULL DEFAULT 1,
            session_active INTEGER NOT NULL DEFAULT 0,
            attempts INTEGER NOT NULL DEFAULT 3,
            blocked_until TEXT
        )
    """)

    cursor.execute("SELECT 1 FROM users WHERE username = ?", ("admin",)) # verifica se existe usuário admin

    if cursor.fetchone() is None: # pega a primeira linha do select, se é None, admin não existe, tipo um ReadLine.
        cursor.execute(
            "INSERT INTO users (username, password, attempts, blocked_until) VALUES (?, ?, ?, ?)",
            ("admin", hash_password("54321"), 3, None)
        )
    
    conn.commit() # salva as mudanças
    conn.close() # fecha a conexão
