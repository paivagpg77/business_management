import streamlit as st
import sqlite3 as sql

conn = sql.connect('database.db', check_same_thread=False)
cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS empresas(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            cnpj TEXT
) 
""")
conn.commit()

st.title('Cadastro da Empresa')

nome = st.text_input("Nome")
cnpj = st.text_input('CNPJ')

if st.button('Cadastrar Dados'):
    cur.execute(
        "INSERT INTO empresas (nome,cnpj)  VALUES (?,?)", 
        (nome , cnpj)
    )
    conn.commit()
    st.success('Empresa cadastrada!')
