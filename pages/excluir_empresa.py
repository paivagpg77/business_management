import streamlit as st
from db import get_connection, deletar_empresa

st.title("Excluir Empresa")

conn = get_connection()
empresas = conn.execute(
    "SELECT id, nome FROM empresas"
).fetchall()
conn.close()

if not empresas:
    st.info("Nenhuma empresa cadastrada.")
else:
    empresa = st.selectbox(
        "Empresa",
        options=empresas,
        format_func=lambda x: x[1]
    )

    confirmacao = st.text_input(
        "Digite o nome da empresa para confirmar"
    )

    st.warning("Essa ação é irreversível.")

    if st.button("Apagar empresa"):
        if confirmacao == empresa[1]:
            deletar_empresa(empresa[0])
            st.success("Empresa apagada com sucesso!")
            st.rerun()
        else:
            st.error("Nome incorreto.")
