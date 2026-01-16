import streamlit as st
from db import get_connection

st.title("Cadastro de Empresa")

conn = get_connection()
cur = conn.cursor()

nome = st.text_input("Nome da empresa")
cnpj = st.text_input("CNPJ")

if st.button("Cadastrar empresa"):
    if nome and cnpj:
        cur.execute(
            "INSERT INTO empresas (nome, cnpj) VALUES (?, ?)",
            (nome, cnpj)
        )
        conn.commit()
        st.success("Empresa cadastrada com sucesso!")
    else:
        st.error("Preencha todos os campos")

conn.close()
