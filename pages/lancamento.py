import streamlit as st
from db import get_connection

conn = get_connection()
cur = conn.cursor()

st.title("Lançamento Fiscal")

empresas = cur.execute(
    "SELECT id, nome FROM empresas"
).fetchall()

if not empresas:
    st.warning("Cadastre uma empresa primeiro.")
else:
    empresa = st.selectbox(
        "Empresa",
        options=empresas,
        format_func=lambda x: x[1]
    )

    mes = st.selectbox(
        "Mês",
        [
            "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
            "Jul", "Ago", "Set", "Out", "Nov", "Dez"
        ]
    )

    receita = st.number_input("Receita", min_value=0.0, step=100.0)
    despesas = st.number_input("Despesas", min_value=0.0, step=100.0)
    impostos = st.number_input("Impostos", min_value=0.0, step=100.0)

    if st.button("Salvar lançamento"):
        cur.execute("""
            INSERT INTO lancamentos
            (empresa_id, mes, receita, despesas, impostos)
            VALUES (?, ?, ?, ?, ?)
        """, (empresa[0], mes, receita, despesas, impostos))

        conn.commit()
        st.success("Lançamento salvo com sucesso!")
