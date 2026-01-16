import sqlite3

def get_connection():
    conn = sqlite3.connect("database.db", check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def criar_tabelas():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS empresas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS lancamentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            empresa_id INTEGER NOT NULL,
            mes TEXT NOT NULL,
            receita REAL,
            despesas REAL,
            impostos REAL,
            FOREIGN KEY (empresa_id) REFERENCES empresas(id)
        )
    """)

    conn.commit()
    conn.close()


def deletar_empresa(empresa_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM lancamentos WHERE empresa_id = ?",
        (empresa_id,)
    )

    cur.execute(
        "DELETE FROM empresas WHERE id = ?",
        (empresa_id,)
    )

    conn.commit()
    conn.close()
